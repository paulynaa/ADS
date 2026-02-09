import matplotlib.pyplot as plt

def plot_results(x_bounds, y_bounds, geros_lokacijos, blogos_lokacijos, universiteto_lokacijos):
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#000000')
    ax.set_xlim(x_bounds[0], x_bounds[1])
    ax.set_ylim(y_bounds[0], y_bounds[1])
    ax.set_aspect('equal', adjustable='box')

    ax.set_facecolor('#171520')

    ax.tick_params(axis='both', colors='#45405c')
    ax.xaxis.label.set_color('#45405c')
    ax.yaxis.label.set_color('#45405c')
    plt.title("Rastos Universiteto lokacijos", color='#dfdfdf')

    ax.grid(True, which='both', linestyle='--', linewidth=0.7, color='#45405c')
    ax.minorticks_on()

    handles, labels = [], []

    def add_plot(x, y, marker, color, label, handles, labels):
        if label not in labels:
            labels.append(label)
            line, = ax.plot(x, y, marker=marker, markersize=6, color=color, label=label)
            handles.append(line)
        else:
            ax.plot(x, y, marker=marker, markersize=6, color=color)

    for gera in geros_lokacijos:
        add_plot(gera[0], gera[1], 's', '#6AFF9B', 'Gera', handles, labels)

    for bloga in blogos_lokacijos:
        add_plot(bloga[0], bloga[1], 's', '#f97e72', 'Bloga', handles, labels)

    for universitetas in universiteto_lokacijos:
        add_plot(universitetas[0], universitetas[1], 'o', '#FFFFFF', 'Universitetas', handles, labels)

    plt.xlabel("X", color='#dfdfdf')
    plt.ylabel("Y", color='#dfdfdf')
    ax.legend(handles=handles, loc='best', facecolor='#171520', edgecolor='#dfdfdf', fontsize='medium', labelcolor='#dfdfdf')
    plt.show()