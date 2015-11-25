import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# calculate step coordinates
def calculate_steps(tableaux, xs=['x_1','x_2']):

    steps = len(tableaux)
    coords = np.zeros([steps, 2])
    values = np.zeros(steps)

    for step in xrange(steps):
        values[step] = tableaux[step].ix[-1,'value']
        x_1_val = tableaux[step].ix[tableaux[step].ix[:,'basic_variable']==xs[0],'value']
        if len(x_1_val) > 0: coords[step, 0] = x_1_val[0]
        x_2_val = tableaux[step].ix[tableaux[step].ix[:,'basic_variable']==xs[1],'value']
        if len(x_2_val) > 0: coords[step, 1] = x_2_val[0]

    return coords, values

# plotting functions
def plot_it(x_1_bounds, x_2_bounds, objective, res=50, title='Graph', xlabel=r'x_1', ylabel=r'x_2', legend_loc=4, constraints=None, constraint_labels=None, auc=True):
    
    fig = plt.figure()
    axes = fig.add_subplot(111)
        
    # plot axes
#     axis_color = '#B3B3B3'
#     axis_width = 5
#     axes.axhline(0, color=axis_color, linewidth=axis_width)
#     axes.axvline(0, color=axis_color, linewidth=axis_width)
    
    # plot objective
    obj_x = np.linspace(x_1_bounds[0], x_1_bounds[1], res)
    obj_y = np.linspace(x_2_bounds[0], x_2_bounds[1], res)
    obj_f = np.empty([obj_x.size, obj_y.size])
    for i, obj_x_i in enumerate(obj_x):
        obj_f[:,i] = objective[0] * obj_x_i + objective[1] * obj_y
    axes.contourf(obj_x, obj_y, obj_f, res, cmap='Oranges', alpha=0.7)
    
    # plot constraints
    const_colors = plt.rcParams['axes.color_cycle']
    n_constraints = constraints.shape[0]
    constraint_width = 1.5
    if constraint_labels==None:
        constraint_labels = np.empty(n_constraints, dtype=object)
        for i in xrange(n_constraints):
            constraint_labels[i] = 'Constraint ' + str(i+1)
    
    def plot_constraint(i):
        # find x intercept
        x_int = constraints[i,2]/constraints[i,0]
        if x_int > 0:
            xs = np.linspace(x_1_bounds[0], min(x_1_bounds[1], x_int), res)
        else:
            xs = np.linspace(x_1_bounds[0], x_1_bounds[1], res)
        ys = (constraints[i,2] - constraints[i,0] * xs) / constraints[i,1]
        axes.plot(xs, ys, label=constraint_labels[i], linewidth=constraint_width, color=const_colors[i])
        # fill under constraints
        if auc==True:
            axes.fill_between(xs, ys, color=const_colors[i], alpha=0.5)
    
    for i in xrange(n_constraints):
        plot_constraint(i)

    # label graph
    axes.set_title(title)
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.legend(loc=legend_loc)

    return axes

def make_tableau(constraints, objective, variables):

    rows = np.concatenate((constraints, objective), axis=0)
    column_names = variables + ['value', 'basic_variable']
    row_names = np.empty(rows.shape[0], dtype=object)
    for i in xrange(rows.shape[0] - 1):
        row_names[i] = 'c_' + str(i+1)
    row_names[-1] = 'z'
    tableau = pd.DataFrame(rows, columns=column_names, index=row_names)
    tableau.ix[:,0:-1] = tableau.ix[:,0:-1].astype('float')

    return tableau
    