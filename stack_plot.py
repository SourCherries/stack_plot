import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------------
# Display parameters.

# Colors.
cmap = 'coolwarm'
# event_color = "#dd1c77"
event_color = "#31a354"

FontSize = 16
plt.rcParams.update({'font.size': FontSize})

# Window position and size.
f_height_inches = 8

# Scalar to stretch y axis range
mult_y = 1.3

# Scalar to stretch color range
mult_c = 1.0

# Vertical line for primary event.
do_vertical_line = True

# Range of x axis in milliseconds.
#   Data range from -1000 to 1000 ms.
xlim_global = [-900, 600]


# --------------------------------------------------------
# Get data - mean ERP across multiple conditions.
subject_id = 7
ms_per_sample = 2
ms = np.arange(start=-1000, stop=1000+ms_per_sample, step=ms_per_sample)
M = np.fromfile("MERP_S" + str(subject_id) + ".bin")
number_waves = 14
number_frames = ms.size
M = M.reshape((-1, number_waves), order='F')
event_a_dur_ms = 250
event_a_ms = np.append(np.arange(0, 600+50, 50) * -1 - event_a_dur_ms, None)

maxAbsY = round(np.abs(M).max() * mult_y)
ylim_global = [-maxAbsY, maxAbsY]

maxAbsC = round(np.abs(M).max() * mult_c)
clim_global = [-maxAbsC, maxAbsC]

# --------------------------------------------------------
# Initial plot to determine appropriate x ticks based on Matplotlib defaults.
fig, axs = plt.subplots(number_waves, 1, sharex=True, sharey=True)
fig.subplots_adjust(hspace=0)
axs[0].scatter(ms, M[:, 0], s=None, c=M[:, 0], cmap=cmap,
               vmin=clim_global[0], vmax=clim_global[1])
axs[0].set_xlim(xlim_global[0], xlim_global[1])
x_ticks = axs[0].get_xticks()
plt.close(fig)


# --------------------------------------------------------
# Plot each time series.
#   Ensure appropriate ranges.
#   Set spines to be invisible except for bottom spine for bottom series.
fig, axs = plt.subplots(number_waves, 1, sharex=False, sharey=False)
fig.subplots_adjust(hspace=0)
for i in range(number_waves):
    sp = axs[i].scatter(ms, M[:, i], s=None, c=M[:, i], cmap=cmap,
                        vmin=clim_global[0], vmax=clim_global[1])
    if event_a_ms[i] is not None:
        e1 = axs[i].plot(event_a_ms[i], 5, '|', ms=14, mew=3, color=event_color)
    else:
        e1 = axs[i].plot(-250, 5, '|', ms=14, mew=3, color=event_color)
        eh = e1[0]
        eh.set_visible(False)

    if not do_vertical_line:
        axs[i].plot(0, 5, '|k', ms=14, mew=3)

    axs[i].set_xlim(xlim_global[0], xlim_global[1])
    axs[i].spines['left'].set_visible(False)
    axs[i].spines['right'].set_visible(False)
    axs[i].spines['bottom'].set_visible(False)
    axs[i].spines['top'].set_visible(False)
    axs[i].set_xticks([])
    axs[i].set_yticks([])
axs[-1].spines['bottom'].set_visible(True)
axs[-1].set_xticks(x_ticks)
xl_txt = "Time since event, milliseconds"
fontdict = {'fontsize': FontSize}
labelpad = 5
plt.xlabel(xl_txt, fontdict=fontdict, labelpad=labelpad)

# Ensure y-axis ranges are uniform and stretched out enough to fit data.
for ax in axs:
    ax.set_ylim(ylim_global)
    ax.set_xlim(xlim_global)

# Colorbar.
cbo = fig.colorbar(sp, ax=axs, shrink=0.6, label="Voltage")

# Vertical line spanning sub plots.
if do_vertical_line:
    xlim_global = ax.get_xlim()
    txp = abs(xlim_global[0])/(xlim_global[1]-xlim_global[0])
    axs[-1].plot([txp, txp], [0, 14], 'k--', transform=axs[-1].transAxes,
                 clip_on=False, ms=14, mew=3)

# Sizing of figure and display.
aspect_ratio = 1.76
w_height_inches = f_height_inches * aspect_ratio
fig.set_size_inches((w_height_inches, f_height_inches))


# -----------------------------------------------------------------
# Title.
t1 = "Neural response to an event is modulated by response to previous event ("
to1 = fig.text(0.45, 0.90, t1, ha="center", va="bottom", fontsize=18,
               color="black")
r = fig.canvas.get_renderer()
fig_w_points = fig.get_size_inches()[0]*fig.dpi

tb = to1.get_window_extent(renderer=r)
tx2 = tb._points_orig[1][0]

# 'bold', 'heavy', 'extra bold', 'black'
to2 = fig.text(tx2 / fig_w_points, 0.90, "  |", ha="center", va="bottom",
               fontsize=18, color=event_color, fontweight="black")

tb = to2.get_window_extent(renderer=r)
tx2 = tb._points_orig[1][0]

to3 = fig.text(tx2 / fig_w_points, 0.90, "  )", ha="center", va="bottom",
               fontsize=18, color="black")


# -----------------------------------------------------------------
# Show and print.
plt.show()

fig.savefig("colored_stack_plot_S" + str(subject_id) + "_" + cmap + ".pdf",
            bbox_inches='tight')
