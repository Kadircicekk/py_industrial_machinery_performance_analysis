import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Bulanık değişkenler
motor_sicakligi = ctrl.Antecedent(np.arange(20, 121, 1), 'motor_sicakligi')
titreşim = ctrl.Antecedent(np.arange(0, 21, 1), 'titreşim')
calisma_hizi = ctrl.Antecedent(np.arange(0, 5001, 1), 'calisma_hizi')
yag_seviyesi = ctrl.Antecedent(np.arange(0, 101, 1), 'yag_seviyesi')
ortam_sicakligi = ctrl.Antecedent(np.arange(0, 51, 1), 'ortam_sicakligi')
performans = ctrl.Consequent(np.arange(0, 11, 1), 'performans')
ariza_riski = ctrl.Consequent(np.arange(0, 101, 1), 'ariza_riski')

# Üyelik fonksiyonları
motor_sicakligi['az'] = fuzz.trimf(motor_sicakligi.universe, [20, 20, 70])
motor_sicakligi['orta'] = fuzz.trimf(motor_sicakligi.universe, [60, 80, 100])
motor_sicakligi['yuksek'] = fuzz.trimf(motor_sicakligi.universe, [90, 120, 120])

titreşim['az'] = fuzz.trimf(titreşim.universe, [0, 0, 7])
titreşim['orta'] = fuzz.trimf(titreşim.universe, [5, 10, 15])
titreşim['yuksek'] = fuzz.trimf(titreşim.universe, [13, 20, 20])

calisma_hizi['az'] = fuzz.trimf(calisma_hizi.universe, [0, 0, 2000])
calisma_hizi['orta'] = fuzz.trimf(calisma_hizi.universe, [1800, 3000, 4000])
calisma_hizi['yuksek'] = fuzz.trimf(calisma_hizi.universe, [3500, 5000, 5000])

yag_seviyesi['az'] = fuzz.trimf(yag_seviyesi.universe, [0, 0, 40])
yag_seviyesi['orta'] = fuzz.trimf(yag_seviyesi.universe, [30, 55, 80])
yag_seviyesi['yuksek'] = fuzz.trimf(yag_seviyesi.universe, [70, 100, 100])

ortam_sicakligi['az'] = fuzz.trimf(ortam_sicakligi.universe, [0, 0, 20])
ortam_sicakligi['orta'] = fuzz.trimf(ortam_sicakligi.universe, [15, 30, 40])
ortam_sicakligi['yuksek'] = fuzz.trimf(ortam_sicakligi.universe, [35, 50, 50])

performans['dusuk'] = fuzz.trimf(performans.universe, [0, 0, 4])
performans['orta'] = fuzz.trimf(performans.universe, [3, 5, 7])
performans['yuksek'] = fuzz.trimf(performans.universe, [6, 10, 10])

ariza_riski['dusuk'] = fuzz.trimf(ariza_riski.universe, [0, 0, 40])
ariza_riski['orta'] = fuzz.trimf(ariza_riski.universe, [30, 50, 70])
ariza_riski['yuksek'] = fuzz.trimf(ariza_riski.universe, [60, 100, 100])

# Kurallar
kurallar = [
    ctrl.Rule(motor_sicakligi['orta'] & titreşim['az'] & calisma_hizi['orta'] & yag_seviyesi['orta'] & ortam_sicakligi['orta'], performans['yuksek']),
    ctrl.Rule(motor_sicakligi['az'] & titreşim['az'] & calisma_hizi['orta'] & yag_seviyesi['yuksek'], performans['orta']),
    ctrl.Rule(motor_sicakligi['yuksek'] | titreşim['yuksek'] | yag_seviyesi['az'], performans['dusuk']),
    ctrl.Rule(ortam_sicakligi['az'] | ortam_sicakligi['yuksek'], performans['orta']),
    ctrl.Rule(calisma_hizi['az'], performans['dusuk']),
    ctrl.Rule(motor_sicakligi['yuksek'] | titreşim['yuksek'] | yag_seviyesi['az'], ariza_riski['yuksek']),
    ctrl.Rule(motor_sicakligi['orta'] & titreşim['orta'] & yag_seviyesi['orta'], ariza_riski['orta']),
    ctrl.Rule(motor_sicakligi['az'] & titreşim['az'] & yag_seviyesi['yuksek'], ariza_riski['dusuk']),
    ctrl.Rule(ortam_sicakligi['yuksek'], ariza_riski['orta']),
    ctrl.Rule(calisma_hizi['yuksek'], ariza_riski['orta']),
    ctrl.Rule(titreşim['orta'] & motor_sicakligi['yuksek'], ariza_riski['yuksek']),
    ctrl.Rule(yag_seviyesi['orta'] & calisma_hizi['orta'], performans['orta']),
    ctrl.Rule(titreşim['orta'] & yag_seviyesi['az'], ariza_riski['yuksek']),
    ctrl.Rule(ortam_sicakligi['orta'] & motor_sicakligi['az'], performans['yuksek']),
    ctrl.Rule(calisma_hizi['yuksek'] & ortam_sicakligi['az'], performans['orta']),
    ctrl.Rule(motor_sicakligi['az'] | titreşim['az'] | yag_seviyesi['yuksek'], ariza_riski['dusuk'])
]

control_system = ctrl.ControlSystem(kurallar)
simulation = ctrl.ControlSystemSimulation(control_system)

# Arayüz
root = tk.Tk()
root.title("Endüstriyel Makine Performans ve Arıza Tahmin Sistemi")
root.geometry("520x510")
root.configure(bg='#1e1e2f')

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background='#1e1e2f', foreground='white', font=('Arial', 12, 'bold'))
style.configure('TEntry', font=('Arial', 12))
style.configure('TButton', background='#4CAF50', foreground='white', font=('Arial', 14, 'bold'))
style.map('TButton', background=[('active', '#45a049')])

frame_inputs = ttk.Frame(root, padding=20)
frame_inputs.pack(fill='x', pady=(10, 5))

labels_text = [
    "Motor Sıcaklığı (20-120 °C):",
    "Titreşim Seviyesi (0-20 mm/s):",
    "Çalışma Hızı (0-5000 rpm):",
    "Yağ Seviyesi (0-100 %):",
    "Ortam Sıcaklığı (0-50 °C):"
]

entries = []
for i, text in enumerate(labels_text):
    lbl = ttk.Label(frame_inputs, text=text)
    lbl.grid(row=i, column=0, sticky='w', pady=5)
    entry = ttk.Entry(frame_inputs, width=20)
    entry.grid(row=i, column=1, pady=5, padx=10)
    entries.append(entry)

entry_motor_sicakligi, entry_titreşim, entry_calisma_hizi, entry_yag_seviyesi, entry_ortam_sicakligi = entries

frame_sonuc = ttk.LabelFrame(root, text="Sonuçlar", padding=15)
frame_sonuc.pack(fill='both', padx=20, pady=10)

label_sonuc = ttk.Label(frame_sonuc, text="Sonuç burada gösterilecek", font=('Arial', 13, 'bold'), justify='center')
label_sonuc.pack(expand=True)

label_author = tk.Label(root, text="Proje Sahibi : Kadir Çiçek", font=('Arial', 10, 'italic'), bg='#1e1e2f', fg='white')
label_author.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


def grafik_goster(perf, ariza, inputs):
    pencere = tk.Toplevel(root)
    pencere.title("Grafikler")

    # Ekran genişlik ve yüksekliğini al
    screen_width = pencere.winfo_screenwidth()
    screen_height = pencere.winfo_screenheight()

    # %90 genişlik ve yükseklik ayarla
    width = int(screen_width * 0.9)
    height = int(screen_height * 0.9)

    # Pencereyi ortala
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    pencere.geometry(f"{width}x{height}+{x}+{y}")

    fig = Figure(figsize=(12, 7), dpi=100)
    renkler = ['blue', 'green', 'orange']

    input_universes = [
        motor_sicakligi.universe,
        titreşim.universe,
        calisma_hizi.universe,
        yag_seviyesi.universe,
        ortam_sicakligi.universe
    ]
    input_mfs = [
        motor_sicakligi.terms,
        titreşim.terms,
        calisma_hizi.terms,
        yag_seviyesi.terms,
        ortam_sicakligi.terms
    ]
    input_labels = ['Motor Sıcaklığı', 'Titreşim', 'Çalışma Hızı', 'Yağ Seviyesi', 'Ortam Sıcaklığı']

    # Giriş değişkenleri için grafikler
    for i in range(5):
        ax = fig.add_subplot(3, 3, i + 1)
        for j, label in enumerate(input_mfs[i]):
            ax.plot(input_universes[i], input_mfs[i][label].mf, label=label, color=renkler[j])
        ax.axvline(inputs[i], color='red', linestyle='--', linewidth=2, label='Girdi')
        ax.set_title(input_labels[i])
        ax.grid(True)
        ax.legend()

    output_universe = np.arange(0, 101, 1)

    # Performans üyelik fonksiyonları
    performans_dusuk = fuzz.trimf(output_universe, [0, 0, 40])
    performans_orta = fuzz.trimf(output_universe, [30, 50, 70])
    performans_yuksek = fuzz.trimf(output_universe, [60, 100, 100])

    # Arıza riski üyelik fonksiyonları
    ariza_dusuk = fuzz.trimf(output_universe, [0, 0, 40])
    ariza_orta = fuzz.trimf(output_universe, [30, 50, 70])
    ariza_yuksek = fuzz.trimf(output_universe, [60, 100, 100])

    # Performans için ayrı grafik
    ax_perf = fig.add_subplot(3, 3, 6)  # 3x3 gridde 6. kutu
    ax_perf.plot(output_universe, performans_dusuk, label='Düşük', color='blue')
    ax_perf.plot(output_universe, performans_orta, label='Orta', color='green')
    ax_perf.plot(output_universe, performans_yuksek, label='Yüksek', color='orange')
    ax_perf.axvline(perf, color='darkgreen', linestyle='--', linewidth=2, label=f'Performans: {perf:.1f}')
    ax_perf.set_title('Performans Üyelik Fonksiyonları')
    ax_perf.set_xlim([0, 100])
    ax_perf.set_ylim([0, 1])
    ax_perf.grid(True)
    ax_perf.legend()

    # Arıza riski için ayrı grafik
    ax_ariza = fig.add_subplot(3, 3, 9)  # 3x3 gridde 9. kutu
    ax_ariza.plot(output_universe, ariza_dusuk, label='Düşük', color='blue', linestyle='dotted')
    ax_ariza.plot(output_universe, ariza_orta, label='Orta', color='green', linestyle='dotted')
    ax_ariza.plot(output_universe, ariza_yuksek, label='Yüksek', color='orange', linestyle='dotted')
    ax_ariza.axvline(ariza, color='darkred', linestyle='--', linewidth=2, label=f'Arıza Riski: {ariza:.1f}')
    ax_ariza.set_title('Arıza Riski Üyelik Fonksiyonları')
    ax_ariza.set_xlim([0, 100])
    ax_ariza.set_ylim([0, 1])
    ax_ariza.grid(True)
    ax_ariza.legend()

    canvas = FigureCanvasTkAgg(fig, master=pencere)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def hesapla():
    try:
        degerler = [
            float(entry_motor_sicakligi.get()),
            float(entry_titreşim.get()),
            float(entry_calisma_hizi.get()),
            float(entry_yag_seviyesi.get()),
            float(entry_ortam_sicakligi.get())
        ]
        keys = ['motor_sicakligi', 'titreşim', 'calisma_hizi', 'yag_seviyesi', 'ortam_sicakligi']
        for key, value in zip(keys, degerler):
            simulation.input[key] = value

        simulation.compute()
        perf = simulation.output['performans']
        ariza = simulation.output['ariza_riski']
        sonuc_yazi = f"Performans: {perf:.2f} / 10\nArıza Riski: {ariza:.2f} %"
        label_sonuc.config(text=sonuc_yazi)
        grafik_goster(perf, ariza, degerler)
    except Exception as e:
        messagebox.showerror("Hata", f"Girişler hatalı ya da eksik!\n{str(e)}")

btn_hesapla = ttk.Button(root, text="Hesapla ve Göster", command=hesapla)
btn_hesapla.pack(pady=10)

root.mainloop()
