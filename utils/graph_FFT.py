
def graph_fft(ax, fft_data):
  ax.set_xlabel("f")
  ax.set_ylabel("y")
  ax.plot(fft_data[0], fft_data[1], label='FFT original')
  ax.grid()
  return