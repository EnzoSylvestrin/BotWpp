from tkinter import Tk, Message, Text, Label, Button, DoubleVar, LEFT, messagebox, ttk
from selenium import webdriver
from time import sleep
from warnings import filterwarnings
#from ConexaoBanco import Banco


class BotWpp:
    def __init__(self):
        filterwarnings("ignore")
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-br")
        # options.add_argument("--headless") caso queira fazer com que o navegador não abra durante o processo
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # opções para não aparecer as mensagens do driver no prompt
        options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=r"./chromedriver.exe")
        self.driver.implicitly_wait(10)

    def MandarMensagem(self, janela, mensagem):
        self.mensagem = mensagem
        c = 0
        lblMsg2 = Label(janela, text="")
        lblMsg2.pack(pady=10)
        var_barra = DoubleVar()
        barra_progresso = ttk.Progressbar(
            janela, variable=var_barra, maximum=len(self.numeros), length=150)
        barra_progresso.pack(pady=8)
        listErro = []
        for numero in self.numeros:
            try:
                lblMsg2['text'] = "Enviando mensagem para o número: " + \
                    (str)(self.numeros[0])
                var_barra.set(c)
                janela.update()
                self.driver.get(
                    "https://api.whatsapp.com/send?phone=55" + (str)(numero))
                btn = self.driver.find_elements_by_tag_name("a")
                btn[73].click()
                btn = self.driver.find_elements_by_tag_name("a")
                btn[76].click()
                sleep(5)
                chatbox = self.driver.find_element_by_class_name("p3_M1")
                chatbox.click()
                chatbox.send_keys(self.mensagem)
                sleep(1)
                try:
                    btnEnviar = self.driver.find_element_by_xpath(
                        "//span[@data-icon='send']")
                    btnEnviar.click()
                    sleep(2)
                    c += 1
                except Exception as e:
                    print(e)
                    chatbox = self.driver.find_element_by_class_name("p3_M1")
                    chatbox.send_keys(self.mensagem)
                    btnEnviar = self.driver.find_element_by_xpath(
                        "//span[@data-icon='send']")
                    btnEnviar.click()
                    c += 1
                    continue
            except Exception as e:
                print(e)
                listErro.append((str)(numero))
                c += 1
                continue
        var_barra.set(c)
        janela.update()
        for contato in self.contatos:
            try:
                cont = self.driver.find_element_by_xpath(
                    f"//span[@title='{contato}']")
                cont.click()
            except Exception:
                print("Número não encontrado")
                listErro.append(contato)
                continue
            sleep(0.5)
            chatbox = self.driver.find_element_by_class_name("p3_M1")
            chatbox.send_keys(self.mensagem)
            sleep(1)
            try:
                btnEnviar = self.driver.find_element_by_xpath(
                    "//span[@data-icon='send']")
                btnEnviar.click()
            except Exception:
                chatbox.send_keys(self.mensagem)
                try:
                    btnEnviar = self.driver.find_element_by_xpath(
                        "//span[@data-icon='send']")
                    btnEnviar.click()
                except Exception:
                    print("Não foi possivel enviar para o contato " +
                          contato + ", passando para o proximo")
                    listErro.append((str)(numero))
                    continue
        sleep(5)
        while (True):
            try:
                btnMenu = self.driver.find_element_by_xpath(
                    "//span[@data-icon='menu']")
                btnMenu.click()
                divDesconect = self.driver.find_element_by_xpath(
                    "//div[@aria-label='Desconectar']")
                divDesconect.click()
            except Exception:
                break
        barra_progresso.pack_forget()
        lbl['text'] = "Script finalizado!!"
        if len(listErro) == 0:
            janela.destroy()
        else:
            cont = 0
            for Erro in listErro:
                if cont == 0:
                    lblMsg2['text'] = "Ocorreram erros com os números: "
                cont += 1
                lblMsg2['text'] += "\n" + Erro
        self.driver.quit()

    def Inicia(self, contatos, numeros):
        if len(numeros) == 0:
            print("Nenhum numero encontrado")
            return
        self.driver.get("https://web.whatsapp.com/")
        self.contatos = contatos
        self.numeros = numeros


def init(estado):
    global lbl, texto, btnConfirm, btnCancel, texto_resposta
    if estado == 1:
        btnConfirm2.pack_forget()
        btnCancel2.pack_forget()
        lblMsg.pack_forget()
    janela.title("Interface Bot Whatsapp")
    if estado == 0:
        lbl = Label(janela, text="Digite a mensagem para que será enviada:")
    else:
        lbl['text'] = "Digite a mensagem para que será enviada:"
    lbl.pack(padx=10, pady=10)
    texto = Text(janela, font=("Arial", "10"), height=10, width=30)
    texto.pack(padx=10, pady=10)
    if estado == 0:
        texto_resposta = Message(janela, text="")
    texto_resposta.pack(padx=10, pady=5)
    texto_resposta.pack_forget()
    btnConfirm = Button(janela, text="Confirmar", command=lambda: Click(0))
    btnCancel = Button(janela, text="Cancelar",
                       command=lambda: janela.destroy())
    btnConfirm.pack(side=LEFT, padx=40, pady=10)
    btnCancel.pack(side=LEFT)


def MudaTela(estado):
    if estado == 0:
        global btnConfirm2, btnCancel2, lblMsg, Bot, abriu
        texto.pack_forget()
        btnConfirm.pack_forget()
        btnCancel.pack_forget()
        lblMsg = Label(janela, text="A mensagem que será enviada é:")
        lblMsg.pack(padx=10, pady=5)
        texto_resposta['text'] = text
        texto_resposta.pack(padx=10, pady=5)
        btnConfirm2 = Button(janela, text="Confirmar",
                             command=lambda: Click(1))
        btnConfirm2.pack(side=LEFT, padx=30, pady=10)
        btnCancel2 = Button(janela, text="Mudar mensagem",
                            command=lambda: init(1))
        btnCancel2.pack(side=LEFT)
        lbl['text'] = "Pronto, agora espere o whatsapp abrir, \n escaneie o QR code e clique em confirmar..."
        if not abriu:
            Bot = BotWpp()
            Bot.Inicia(["Coloque os contatos aqui"],
                       ["Coloque os números aqui"])
            abriu = True
    else:
        lblMsg.pack_forget()
        btnCancel2.pack_forget()
        btnConfirm2.pack_forget()
        texto_resposta.pack_forget()
        lbl['text'] = "Sucesso, o script está rodando \n por favor não feche essa janela."
        Bot.MandarMensagem(janela, text)


def Click(estado):
    global text
    if estado == 0:
        text = texto.get("1.0", "end").strip()
        MudaTela(0)
    else:
        Msg = messagebox.askokcancel(
            "Aviso...", "Você tem certeza que irá mandar essa mensagem para os clientes? \n\nObs: Caso o navegador esteja fechado, ou o whatsapp web não esteja aberto o script irá falhar.")
        if Msg:
            MudaTela(1)


abriu = False
janela = Tk()
janela.resizable(False, False)
init(0)
janela.mainloop()
