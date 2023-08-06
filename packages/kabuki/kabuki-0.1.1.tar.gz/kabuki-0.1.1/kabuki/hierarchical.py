 #!/usr/bin/python
from __future__ import division
from copy import copy

import numpy as np
import numpy.lib.recfunctions as rec
from ordereddict import OrderedDict

import pymc as pm

import kabuki

class Parameter(object):
    """Specify a parameter of a model.

    :Arguments:
        name <str>: Name of parameter.

    :Keyword arguments:
        has_root <bool=True>: Parameter has a root node.
        lower <float>: Lower bound (e.g. for a uniform distribution).
        upper <float>: Upper bound (e.g. for a uniform distribution).
        init <float>: Initialize to value.
        vars <dict>: User-defined variables, can be anything you later
            want to access.
        optional <bool=False>: Only create distribution when included. 
            Otherwise, set to default value (see below).
        default <float>: Default value if optional=True.
        no_childs <bool=False>: Do not create children nodes.
        verbose <int=0>: Verbosity.
    """

    def __init__(self, name, has_root=True, lower=None, upper=None, init=None, vars=None, default=None, no_childs=False, optional=False, verbose=0):
        self.name = name
        self.has_root = has_root
        self.lower = lower
        self.upper = upper
        self.init = init
        self.vars = vars
        self.no_childs = no_childs
        self.optional = optional
        self.default = default
        self.verbose = verbose
        
        if self.optional and self.default is None:
            raise ValueError("Optional parameters have to have a default value.")

        self.root_nodes = OrderedDict()
        self.tau_nodes = OrderedDict()
        self.child_nodes = OrderedDict()

        # Pointers that get overwritten
        self.root = None
        self.child = None
        self.tag = None
        self.data = None
        self.idx = None

    def reset(self):
        self.root = None
        self.child = None
        self.tag = None
        self.data = None
        self.idx = None

    def get_full_name(self):
        if self.idx is not None:
            if self.tag is not None:
                return '%s%s%i'%(self.name, self.tag, self.idx)
            else:
                return '%s%i'%(self.name, self.idx)
        else:
            if self.tag is not None:
                return '%s%s'%(self.name, self.tag)
            else:
                return self.name

    full_name = property(get_full_name)

    def __repr__(self):
        return object.__repr__(self).replace(' object ', " '%s' "%self.name)

    
class Hierarchical(object):
    """Creation of hierarchical Bayesian models in which each subject
    has a set of parameters that are constrained by a group distribution.

    :Arguments:
        data : numpy.recarray
            Input data with a row for each trial.
            Must contain the following columns:
              * 'rt': Reaction time of trial in seconds.
              * 'response': Binary response (e.g. 0->error, 1->correct)
            May contain:
              * 'subj_idx': A unique ID (int) of the subject.
              * Other user-defined columns that can be used in depends_on
                keyword.

    :Optional:
        include : tuple
            If the model has optional arguments, they
            can be included as a tuple of strings here.

        is_group_model : bool 
            If True, this results in a hierarchical
            model with separate parameter distributions for each
            subject. The subject parameter distributions are
            themselves distributed according to a group parameter
            distribution.
        
        depends_on : dict
            Specifies which parameter depends on data
            of a column in data. For each unique element in that
            column, a separate set of parameter distributions will be
            created and applied. Multiple columns can be specified in
            a sequential container (e.g. list)

            :Example: 

            >>> depends_on={'param1':['column1']}
    
            Suppose column1 has the elements 'element1' and
            'element2', then parameters 'param1('element1',)' and
            'param1('element2',)' will be created and the
            corresponding parameter distribution and data will be
            provided to the user-specified method get_liklihood().

        trace_subjs : bool
             Save trace for subjs (needed for many
             statistics so probably a good idea.)

        plot_tau : bool
             Plot group variability parameters
             (i.e. variance of Normal distribution.)

    :Note: 
        This class must be inherited. The child class must provide
        the following functions:
            * get_root_node(param): Return group mean distribution for param.
            * get_tau_node(param): Return group variability distribution for param.
            * get_child_node(param): Return subject distribution for param.
            * get_rootless_child(param, params): Return distribution
                  for rootless param (e.g. the model
                  likelihood). params contains the associated model
                  parameters.

        In addition, the variable self.params must be defined as a
        list of Paramater().

    """

    def __init__(self, data, is_group_model=None, depends_on=None, trace_subjs=True, plot_subjs=False, plot_tau=False, include=()):
        # Init
        self.include = set(include)
        
        self.nodes = {}
        self.mc = None
        self.trace_subjs = trace_subjs
        self.plot_subjs = plot_subjs
        self.plot_tau = plot_tau

        if not depends_on:
            self.depends_on = {}
        else:
            # Support for supplying columns as a single string
            # -> transform to list
            for key in depends_on:
                if type(depends_on[key]) is str:
                    depends_on[key] = [depends_on[key]]
            # Check if column names exist in data        
            for depend_on in depends_on.itervalues():
                for elem in depend_on:
                    if elem not in self.data.dtype.names:
                        raise KeyError, "Column named %s not found in data." % elem
            self.depends_on = depends_on

        if is_group_model is None:
            if 'subj_idx' in data.dtype.names:
                if len(np.unique(data['subj_idx'])) != 1:
                    self.is_group_model = True
                else:
                    self.is_group_model = False
            else:
                self.is_group_model = False

        else:
            if is_group_model:
                if 'subj_idx' not in data.dtype.names:
                    raise ValueError("Group models require 'subj_idx' column in input data.")

            self.is_group_model = is_group_model

        # Should the model incorporate multiple subjects
        if self.is_group_model:
            self._subjs = np.unique(data['subj_idx'])
            self._num_subjs = self._subjs.shape[0]

            
    def _get_data_depend(self):
        """Partition data according to self.depends_on.

        :Returns:
            List of tuples with the data, the corresponding parameter
            distribution and the parameter name.

        """
        
        params = {} # use subj parameters to feed into model
        # Create new params dict and copy over nodes
        for name, param in self.params_include.iteritems():
            if name in self.depends_on or not param.has_root:
                continue
            if self.is_group_model and not param.no_childs:
                params[name] = param.child_nodes['']
            else:
                params[name] = param.root_nodes['']

        depends_on = copy(self.depends_on)

        # Make call to recursive function that does the partitioning
        data_dep = self._get_data_depend_rec(self.data, depends_on, params, [])

        return data_dep
    
    def _get_data_depend_rec(self, data, depends_on, params, dep_name, param=None):
        """Recursive function to partition data and params according
        to depends_on.

        """
        if len(depends_on) != 0: # If depends are present
            data_params = []
            # Get first param from depends_on
            param_name = depends_on.keys()[0]
            col_name = depends_on.pop(param_name) # Take out param
            depend_elements = np.unique(data[col_name])
            # Loop through unique elements
            for depend_element in depend_elements:
                # Append dependent element name.
                dep_name.append(depend_element)
                # Extract rows containing unique element
                data_dep = data[data[col_name] == depend_element]

                # Add a key that is only the col_name that links to
                # the correct dependent nodes. This is the central
                # trick so that later on the get_rootless_child can use
                # params[col_name] and the observed will get linked to
                # the correct nodes automatically.
                param = self.params_include[param_name]

                # Add the node
                if self.is_group_model and not param.no_childs:
                    params[param_name] = param.child_nodes[str(depend_element)]
                else:
                    params[param_name] = param.root_nodes[str(depend_element)]
                # Recursive call with one less dependency and the selected data.
                data_param = self._get_data_depend_rec(data_dep,
                                                       depends_on=copy(depends_on),
                                                       params=copy(params),
                                                       dep_name = copy(dep_name),
                                                       param = param)
                data_params += data_param
                # Remove last item (otherwise we would always keep
                # adding the dep elems of in one column)
                dep_name.pop()
            return data_params
                
        else: # Data does not depend on anything (anymore)
            return [(data, params, dep_name)]

    def create_nodes(self, retry=20):
        """Set group level distributions. One distribution for each
        parameter.

        :Arguments:
            retry : int
                How often to retry when model creation 
                failed (due to bad starting values).

        """
        def _create():
            for name, param in self.params_include.iteritems():
                if not param.has_root:
                    continue
                # Check if parameter depends on data
                if name in self.depends_on.keys():
                    self._set_dependent_param(param)
                else:
                    self._set_independet_param(param)

        # Include all defined parameters by default.
        self.non_optional_params = [param.name for param in self.params if not param.optional]

        # Create params dictionary
        self.params_dict = OrderedDict()
        for param in self.params:
            self.params_dict[param.name] = param
        self.params_include = OrderedDict()
        for param in self.params:
            if param.name in self.include or not param.optional:
                self.params_include[param.name] = param

        succeeded = False
        tries = 0
        while(not succeeded):
            try:
                _create()
                succeeded = True
            except (pm.ZeroProbability, ValueError) as e:
                if tries < retry:
                    tries += 1
                else:
                    raise pm.ZeroProbability, e
        
        # Init rootless nodes
        for param in self.params_include.itervalues():
            if param.has_root:
                continue
            self._set_rootless_child_nodes(param, init=True)

        # Create rootless nodes
        for param in self.params_include.itervalues():
            if param.has_root:
                continue
            self._set_rootless_child_nodes(param, init=False)

        # Create model dictionary
        self.nodes = {}
        for name, param in self.params_include.iteritems():
            for tag, node in param.root_nodes.iteritems():
                self.nodes[name+tag+'_root'] = node
            for tag, node in param.child_nodes.iteritems():
                self.nodes[name+tag+'_child'] = node
            for tag, node in param.tau_nodes.iteritems():
                self.nodes[name+tag+'_tau'] = node

        return self.nodes
    
    def mcmc(self, *args, **kwargs):
        """
        Returns pymc.MCMC object of model.

        :Note:
            Forwards arguments to pymc.MCMC().

        """

        if not self.nodes:
            self.create_nodes()

        self.mc = pm.MCMC(self.nodes, *args, **kwargs)
        
        if kwargs.has_key('dbname'):
            self.mc.db.close()

        return self.mc

    def sample(self, *args, **kwargs):
        """Sample from posterior.
        
        :Note:
            Forwards arguments to pymc.MCMC.sample().

        """
        if not self.mc:
            self.mcmc()
        
        self.mc.sample(*args, **kwargs)
        
        return self.mc

    def print_group_stats(self):
        if not self.mc:
            raise ValueError("No model found.")
            
        kabuki.analyze.print_group_stats(self.mc.stats())

    def print_stats(self):
        if not self.mc:
            raise ValueError("No model found.")
            
        kabuki.analyze.print_stats(self.mc.stats())

    def _set_dependent_param(self, param):
        """Set parameter that depends on data.

        :Arguments:
            param_name : string
                Name of parameter that depends on data for
                which to set distributions.

        """

        # Get column names for provided param_name
        depends_on = self.depends_on[param.name]

        # Get unique elements from the columns
        data_dep = self.data[depends_on]
        uniq_data_dep = np.unique(data_dep)

        # Loop through unique elements
        for uniq_date in uniq_data_dep:
            # Select data
            data_dep_select = self.data[(data_dep == uniq_date)]

            # Create name for parameter
            tag = str(uniq_date)

            # Create parameter distribution from factory
            param.tag = tag
            param.data = data_dep_select
            param.root_nodes[tag] = self.get_root_node(param)
            param.reset()

            if self.is_group_model and not param.no_childs:
                # Create appropriate subj parameter
                self._set_child_nodes(param, tag, data_dep_select)

        return self

    def _set_independet_param(self, param):
        """Set parameter that does _not_ depend on data.

        :Arguments:
            param_name : string
                Name of parameter.

        """

        # Parameter does not depend on data
        # Set group parameter
        param.tag = ''
        param.root_nodes[''] = self.get_root_node(param)
        param.reset()

        if self.is_group_model and not param.no_childs:
            self._set_child_nodes(param, '', self.data)
        
        return self

    def _set_child_nodes(self, param, tag, data):
        """Set nodes with a parent.

        :Arguments:
            param_name : string
                Name of parameter.
            tag : string
                Element name.
            data : numpy.recarray
                Part of the data the parameter 
                depends on.

        """
        # Generate subj variability parameter tau
        param.tag = 'tau'+tag
        param.data = data
        param.tau_nodes[tag] = self.get_tau_node(param)
        param.reset()

        # Init
        param.child_nodes[tag] = np.empty(self._num_subjs, dtype=object)
        # Create subj parameter distribution for each subject
        for subj_idx,subj in enumerate(self._subjs):
            data_subj = data[data['subj_idx']==subj]
            param.data = data_subj
            param.root = param.root_nodes[tag]
            param.tau = param.tau_nodes[tag]
            param.tag = tag
            param.idx = subj_idx
            param.child_nodes[tag][subj_idx] = self.get_child_node(param)
            param.reset()

        return self
    
    def _set_rootless_child_nodes(self, param, init=False):
        """Set parameter node that has no parent.

        :Arguments:
            param_name : string
                Name of parameter.
        
        :Optional:
            init : bool
                Initialize parameter.

        """
        # Divide data and parameter distributions according to self.depends_on
        data_dep = self._get_data_depend()

        # Loop through parceled data and params and create an observed stochastic
        for i, (data, params_dep, dep_name) in enumerate(data_dep):
            dep_name = str(dep_name)
            if init:
                if self.is_group_model and not param.no_childs:
                    param.child_nodes[dep_name] = np.empty(self._num_subjs, dtype=object)
                else:
                    param.child_nodes[dep_name] = None
            else:
                self._create_rootless_child_node(param, data, params_dep, dep_name, i)
            
        return self
        
    def _create_rootless_child_node(self, param, data, params, dep_name, idx):
        """Create parameter node object which has no parent.

        :Note: 
            Called by self._set_rootless_child_node().

        :Arguments:
            param_name : string
                Name of parameter.
            data : numpy.recarray
                Data on which parameter depends on.
            params : list
                List of parameters the node depends on.
            dep_name : str
                Element name the node depends on.
            idx : int
                Subject index.
        
        """
        if self.is_group_model:
            for i,subj in enumerate(self._subjs):
                # Select data belonging to subj
                data_subj = data[data['subj_idx'] == subj]
                # Skip if subject was not tested on this condition
                if len(data_subj) == 0:
                    continue
                # Select params belonging to subject
                selected_child_nodes = {}
                # Create new params dict and copy over nodes
                for selected_param in self.params_include.itervalues():
                    # Since rootless nodes are not created in this function we
                    # have to search for the correct node and include it in
                    # the params.
                    if selected_param.no_childs:
                        if selected_param.child_nodes.has_key(dep_name):
                            selected_child_nodes[selected_param.name] = selected_param.root_nodes[dep_name]
                        else:
                            selected_child_nodes[selected_param.name] = params[selected_param.name]
                    else:
                        if selected_param.child_nodes.has_key(dep_name):
                            selected_child_nodes[selected_param.name] = selected_param.child_nodes[dep_name][i]
                        else:
                            selected_child_nodes[selected_param.name] = params[selected_param.name][i]

                # Call to the user-defined function!
                param.tag = dep_name
                param.idx = i
                param.data = data_subj
                param.child_nodes[dep_name][i] = self.get_rootless_child(param, selected_child_nodes)
                param.reset()
        else: # Do not use subj params, but group ones
            # Since rootless nodes are not created in this function we
            # have to search for the correct node and include it in
            # the params
            for selected_param in self.params_include.itervalues():
                if selected_param.child_nodes.has_key(dep_name):
                    params[selected_param.name] = selected_param.child_nodes[dep_name]
            param.tag = dep_name
            param.data = data
            param.child_nodes[dep_name] = self.get_rootless_child(param, params)
            param.reset()

        return self

    def compare_all_pairwise(self):
        """Perform all pairwise comparisons of dependent parameter
        distributions (as indicated by depends_on).

        :Stats generated:
            * Mean difference
            * 5th and 95th percentile

        """
        from scipy.stats import scoreatpercentile
        from itertools import combinations

        print "Parameters\tMean difference\t5%\t95%"
        # Loop through dependent parameters and generate stats
        for params in self.root_nodes_dep.itervalues():
            # Loop through all pairwise combinations
            for p0,p1 in combinations(params, 2):
                diff = self.root_nodes[p0].trace()-self.root_nodes[p1].trace()
                perc_5 = scoreatpercentile(diff, 5)
                perc_95 = scoreatpercentile(diff, 95)
                print "%s vs %s\t%.3f\t%.3f\t%.3f" %(p0, p1, np.mean(diff), perc_5, perc_95)

    def plot_all_pairwise(self):
        """Plot all pairwise posteriors to find correlations."""
        import matplotlib.pyplot as plt
        import scipy as sp
        import scipy.stats
        #size = int(np.ceil(np.sqrt(len(data_deps))))
        fig = plt.figure()
        fig.subplots_adjust(wspace=0.4, hspace=0.4)
        # Loop through all pairwise combinations
        for i,(p0,p1) in enumerate(kabuki.utils.all_pairs(self.root_nodes.values())):
            fig.add_subplot(6,6,i+1)
            plt.plot(p0.trace(), p1.trace(), '.')
            (a_s,b_s,r,tt,stderr) = sp.stats.linregress(p0.trace(), p1.trace())
            reg = sp.polyval((a_s, b_s), (np.min(p0.trace()), np.max(p0.trace())))
            plt.plot((np.min(p0.trace()), np.max(p0.trace())), reg, '-')
            plt.xlabel(p0.__name__)
            plt.ylabel(p1.__name__)
            
            #plt.plot

    def get_node(self, node_name, params):
        """Returns the node object with node_name from params if node
        is included in model, otherwise returns default value.

        """
        if node_name in self.include:
            return params[node_name]
        else:
            assert self.params_dict[node_name].default is not None, "Default value of not-included parameter not set."
            return self.params_dict[node_name].default
