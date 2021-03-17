import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib
from gempy.plot.visualization_2d import Plot2D

lith = None
hill = None

def plot_gempy_topography(ax,
                          geo_model,
                          extent,
                          show_lith: bool = True,
                          show_boundary: bool = True,
                          show_hillshade: bool = True,
                          show_contour: bool = False,
                          **kwargs):
    """
    Use the native plotting function class of gempy to plot the lithology, boundaries and hillshading.
    Args:
        ax: axes of sandbox to paint in
        geo_model: geo_model from gempy
        extent:
        show_lith: default True
        show_boundary: default True
        show_hillshade: default True
        show_contour: default False (using native sandbox contours)
    Returns:

    """
    cmap = mcolors.ListedColormap(list(geo_model._surfaces.df['color']))
    delete_ax(ax)
    p = Plot2D(geo_model)
    p.fig = ax.figure
    p.add_section(ax=ax, section_name="topography")
    if show_lith:
        p.plot_lith(ax, section_name="topography")
    if show_boundary:
        p.plot_contacts(ax, only_faults=True, section_name="topography")

    if show_hillshade or show_contour:
        p.plot_topography(ax,
                          contour=show_contour,
                          # fill_contour=True,
                          hillshade=show_hillshade,
                          # cmap= cmap,
                          section_name="topography")
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # ax.set_title("")
    return ax, cmap


def plot_gempy(ax,
               geo_model,
               extent,
               show_lith: bool = True,
               show_boundary: bool = True,
               show_hillshade: bool = True,
               show_contour: bool = False,
               show_only_faults: bool = False,
               **kwargs):
    """
    Use the native plotting function class of gempy to plot the lithology, boundaries and hillshading.
    Args:
        ax: axes of sandbox to paint in
        geo_model: geo_model from gempy
        extent:
        show_lith: default True
        show_boundary: default True
        show_hillshade: default True
        show_contour: default False (using native sandbox contours)
        show_only_faults: plot only the fault lines
    Returns:

    """
    cmap = mcolors.ListedColormap(list(geo_model._surfaces.df['color']))
    norm = mcolors.Normalize(vmin=0.5, vmax=len(cmap.colors) + 0.5)
    # color_dir = dict(zip(self.model._surfaces.df['surface'], self.model._surfaces.df['color']))
    extent_val = extent[:4]  # [*ax.get_xlim(), *ax.get_ylim()]
    delete_ax(ax)
    if show_lith:
        # Todo: use instead native cmap module of sandbox
        plot_lith(ax, geo_model, extent_val, cmap, norm)
    if show_boundary:
        plot_contacts(ax, geo_model, extent_val, cmap, only_faults=show_only_faults)
    if show_hillshade or show_contour:
        plot_topography(ax,
                        geo_model,
                        extent_val,
                        show_hillshade=show_hillshade,
                        show_contour=show_contour,
                        **kwargs)
    ax.set_axis_off()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(extent_val[0], extent_val[1])
    ax.set_ylim(extent_val[2], extent_val[3])
    return ax, cmap


def plot_lith(ax, geo_model, extent_val, cmap, norm):
    """

    Args:
        ax: sandbox axes
        geo_model: gempy geo_model
        extent_val: extent x and y of the model
        cmap:
        norm:

    Returns:

    """
    image = geo_model.solutions.geological_map[0].reshape(
        geo_model._grid.topography.values_2d[:, :, 2].shape)
    global lith
    lith = ax.imshow(image, origin='lower', zorder=-10, extent=extent_val, cmap=cmap, norm=norm, aspect='auto')


def plot_contacts(ax, geo_model, extent_val, cmap, only_faults=False):
    """

    Args:
        ax:
        geo_model:
        extent_val:
        cmap:
        only_faults:

    Returns:

    """
    zorder = 100
    if only_faults:
        contour_idx = list(geo_model._faults.df[geo_model._faults.df['isFault'] == True].index)
    else:
        contour_idx = list(geo_model._surfaces.df.index)

    shape = geo_model._grid.topography.resolution

    scalar_fields = geo_model.solutions.geological_map[1]
    c_id = 0  # color id startpoint

    for e, block in enumerate(scalar_fields):
        level = geo_model.solutions.scalar_field_at_surface_points[e][np.where(
            geo_model.solutions.scalar_field_at_surface_points[e] != 0)]

        c_id2 = c_id + len(level)  # color id endpoint
        ax.contour(block.reshape(shape), 0, levels=np.sort(level),
                   colors=cmap.colors[c_id:c_id2][::-1],
                   linestyles='solid', origin='lower',
                   extent=extent_val, zorder=zorder - (e + len(level))
                   )
        c_id = c_id2


def plot_topography(ax, geo_model, extent_val, **kwargs):
    """

    Args:
        ax:
        geo_model:
        extent_val:
        **kwargs:

    Returns:

    """
    hillshade = kwargs.pop('show_hillshade', True)
    contour = kwargs.pop('show_contour', False)
    fill_contour = kwargs.pop('show_fill_contour', False)
    azdeg = kwargs.pop('azdeg', 0)
    altdeg = kwargs.pop('altdeg', 0)
    cmap = kwargs.pop('cmap', 'terrain')
    super = kwargs.pop('super_res', False)
    colorbar = kwargs.pop("show_colorbar", False)

    topo = geo_model._grid.topography
    if super:
        import skimage
        topo_super_res = skimage.transform.resize(
            topo.values_2d,
            (1600, 1600),
            order=3,
            mode='edge',
            anti_aliasing=True, preserve_range=False)
        values = topo_super_res[..., 2]
    else:
        values = topo.values_2d[..., 2]

    if contour is True:
        CS = ax.contour(values, extent=extent_val,
                        colors='k', linestyles='solid', origin='lower')
        ax.clabel(CS, inline=1, fontsize=10, fmt='%d')
    if fill_contour is True:
        CS2 = ax.contourf(values, extent=extent_val, cmap=cmap)
        if colorbar:
            from gempy.plot.helpers import add_colorbar
            add_colorbar(axes=ax, label='elevation [m]', cs=CS2)

    if hillshade is True:
        from matplotlib.colors import LightSource
        # Note: 180 degrees are subtracted because visualization in Sandbox is upside-down
        ls = LightSource(azdeg=azdeg - 180, altdeg=altdeg)
        # TODO: Is is better to use ls.hillshade or ls.shade??
        hillshade_topography = ls.hillshade(values)
                                        # vert_exag=0.3,
                                        # blend_mode='overlay')
        global hill
        hill = ax.imshow(hillshade_topography,
                         cmap=plt.cm.gray,
                         origin='lower',
                         extent=extent_val,
                         alpha=0.4,
                         zorder=11,
                         aspect='auto')


def delete_ax(ax):
    """
    replace the ax.cla(). delete contour fill and images of hillshade and lithology
    Args:
        ax:
    Returns:
        ax
    """
    global lith, hill
    if lith is not None:
        lith.remove()
        lith = None
    if hill is not None:
        hill.remove()
        hill = None
    [fill.remove() for fill in reversed(ax.collections) if isinstance(fill, matplotlib.collections.PathCollection)]
    [coll.remove() for coll in reversed(ax.collections) if isinstance(coll, matplotlib.collections.LineCollection)]
    [text.remove() for text in reversed(ax.artists) if isinstance(text, matplotlib.text.Text)]
    return ax
