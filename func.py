import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def gen_hologram(fig, alpha=0, beta=0, wavelen=5.32e-7, a=0.01, b=0.01, l0=0.1, d=5.2e-6, good=0):
    k = 2 * np.pi / wavelen
    i0 = 0.3 * fig[:, :, 0] + 0.6 * fig[:, :, 1] + 0.1 * fig[:, :, 2]
    n, m = i0.shape
    x = np.linspace(-a / 2, a / 2, m)
    y = np.linspace(-b / 2, b / 2, n)
    u, v = np.meshgrid(x, y)
    u1 = (u / a) * m * d
    v1 = (v / b) * n * d

    c = np.exp(1j * k * l0) / (1j * wavelen * l0)
    e = c * np.exp(1j * k / (2 * l0) * (u1 ** 2 + v1 ** 2)) * np.fft.fftshift(
        np.fft.fft2(i0 * np.exp(1j * k / (2 * l0) * (u ** 2 + v ** 2 - 2 * u * u1 - 2 * v * v1))))
    abs_e = np.max(e)
    e /= abs_e
    r = np.exp(1j * k * u1 * np.sin(beta) + 1j * k * v1 * np.sin(alpha))
    i = (np.abs(e + r)) ** 2
    if good:
        i -= (np.abs(e)) ** 2 + (np.abs(r)) ** 2
    i /= np.max(i)
    i *= 255
    img = Image.new('L', (m, n))
    for x in range(m):
        for y in range(n):
            img.putpixel((x, y), int(i[y][x]))
    img.save("D:/code/PycharmProjects/作业/全息/全息图.bmp")
    return i


def re_hologram(fig, alpha=0, beta=0, wavelen=5.32e-7, a=0.01, b=0.01, l0=0.2, d=5.2e-6):
    try:
        i0 = 0.3 * fig[:, :, 0] + 0.6 * fig[:, :, 1] + 0.1 * fig[:, :, 2]
    except:
        i0 = fig
    k = 2 * np.pi / wavelen
    n, m = i0.shape
    x = np.linspace(-a / 2, a / 2, m)
    y = np.linspace(-b / 2, b / 2, n)
    u, v = np.meshgrid(x, y)
    u1 = (u / a) * m * d
    v1 = (v / b) * n * d

    x = np.linspace(-a / 2, a / 2, m)
    y = np.linspace(-b / 2, b / 2, n)
    u2, v2 = np.meshgrid(x, y)

    c = np.exp(1j * k * l0) / (1j * wavelen * l0)
    r = np.exp(1j * k * u1 * np.sin(beta) + 1j * k * v1 * np.sin(alpha))
    et = c * np.exp(1j * k / (2 * l0) * (u2 ** 2 + v2 ** 2)) * np.fft.fftshift(
        np.fft.fft2(i0 * r * np.exp(1j * k / (2 * l0) * (u1 ** 2 + v1 ** 2))))
    it = (np.abs(et)) ** 2
    it -= np.min(it)
    it /= np.max(it)
    for x in range(m):
        for y in range(n):
            if it[y][x] > 0.01:
                it[y][x] = 0.01
            elif it[y][x] < 0.001:
                it[y][x] = 0
    it /= np.max(it)
    it *= 255
    return it


def two_change(fig1, fig2):
    i0 = 0.3 * fig1[:, :, 0] + 0.6 * fig1[:, :, 1] + 0.1 * fig1[:, :, 2]
    i = 0.3 * fig2[:, :, 0] + 0.6 * fig2[:, :, 1] + 0.1 * fig2[:, :, 2]
    i0 -= i
    i0 -= np.min(i0)

    return i0


def plot(holo, holo_=None, s=False):
    if s:
        plt.subplot(1, 2, 1)
        plt.imshow(holo.real, cmap='gray')
        plt.subplot(1, 2, 2)
        plt.imshow(holo_.real, cmap='gray')
    else:
        plt.subplot(1, 1, 1)
        plt.imshow(holo.real, cmap='gray')
    plt.show()


def perfect_hologram(fig, alpha=0, beta=0, wavelen=5.32e-7, a=0.01, b=0.01, l0=0.1, d=5.2e-6):
    k = 2 * np.pi / wavelen
    i0 = 0.3 * fig[:, :, 0] + 0.6 * fig[:, :, 1] + 0.1 * fig[:, :, 2]
    n, m = i0.shape

    x = np.linspace(-a / 2, a / 2, m)
    y = np.linspace(-b / 2, b / 2, n)
    u, v = np.meshgrid(x, y)
    u1 = (u / a) * m * d
    v1 = (v / b) * n * d

    x = np.linspace(-a / 2, a / 2, m)
    y = np.linspace(-b / 2, b / 2, n)
    u2, v2 = np.meshgrid(x, y)

    c = np.exp(1j * k * l0) / (1j * wavelen * l0)
    e = c * np.exp(1j * k / (2 * l0) * (u1 ** 2 + v1 ** 2)) * np.fft.fftshift(
        np.fft.fft2(i0 * np.exp(1j * k / (2 * l0) * (u ** 2 + v ** 2))))
    abs_e = np.max(e)
    e /= abs_e
    r1 = np.exp(1j * k * u1 * np.sin(beta) + 1j * k * v1 * np.sin(alpha))
    r2 = 1j * r1
    r3 = -r1
    r4 = -1j * r1
    i1 = (np.abs(e + r1)) ** 2
    i2 = (np.abs(e + r2)) ** 2
    i3 = (np.abs(e + r3)) ** 2
    i4 = (np.abs(e + r4)) ** 2

    i = i1 - 1j * i2 - i3 + 1j * i4

    et = c * np.exp(1j * k / (2 * l0) * (u2 ** 2 + v2 ** 2)) * np.fft.fftshift(
        np.fft.fft2(i * r1 * np.exp(1j * k / (2 * l0) * (u1 ** 2 + v1 ** 2))))
    i = np.abs(et) ** 2
    return i


def add_hologram(fig, fig1):
    try:
        i0 = 0.3 * fig[:, :, 0] + 0.6 * fig[:, :, 1] + 0.1 * fig[:, :, 2]
    except:
        i0 = fig
    try:
        i1 = 0.3 * fig1[:, :, 0] + 0.6 * fig1[:, :, 1] + 0.1 * fig1[:, :, 2]
    except:
        i1 = fig1
    i0 -= i1
    i0 -= np.min(i0)
    i0 /= np.max(i0)
    i0 *= 255
    m, n = i0.shape
    img = Image.new('L', (m, n))
    for x in range(m):
        for y in range(n):
            img.putpixel((x, y), int(i0[y][x]))
    img.save("D:/code/PycharmProjects/作业/全息/合成图.bmp")
    return i0
