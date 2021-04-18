class FileN_to_FileC:
    def __init__(self, FNam, FCon):
        self.File_Name = FNam
        self.File_Contents = FCon
    def Breakdown_Contents(self, Break_Catalyst="\n"):
        self.File_Contents = self.File_Contents.split(Break_Catalyst)
def Generate():
    #Opening Sample File to gather the fist initial files that aren't Images
    Fnb = open("Sample.IXXCF", "rb").read().split(b"\r\n|I*X*X|\r\n") #Fnb - File-non binary
    Fnb.remove(Fnb[0])
    Fnb.remove(Fnb[len(Fnb)-1])
    MGL = [] #Master Generator List
    for File in Fnb:
        Temp_List = File.split(b"/:>\r\n")
        MGL.append(FileN_to_FileC(Temp_List[0], Temp_List[1]))
    for Item in MGL:
        Item.Breakdown_Contents(b"\r\n")
    for N_F in MGL:
        Written = open(N_F.File_Name, "w")
        Write_Var = ""
        print("||",N_F.File_Contents)
        for Line in N_F.File_Contents:
            if Line == "\r\n":
                pass
            elif N_F.File_Contents[N_F.File_Contents.index(Line)] == "":
                pass
            else:
                Write_Var += str(Line)+"\n"
        Write_Var = Write_Var.replace("|U", "U").replace("|F", "F").replace("||", "")
        print(Write_Var)
        Write_Var = Write_Var.replace("|", "\n")
        Fin = Write_Var.split("\n")
        Fin.pop(len(Fin)-1)
        Write_Var = ""
        Count = 0
        print("Len:", len(Fin))
        for I in Fin:
            if Count == len(Fin)-1:
                Write_Var += I
            else:
                Write_Var += I+"\n"
            Count += 1
        Written.write(str(Write_Var).replace("b'", "").replace("'", ""))
    #Open and use the Binary version for the Icon
    Fb = open("Sample.IXXCF", "rb").read().split(b"\r\n|I*X*X|\r\n")
    Fin_Bin = Fb.pop(len(Fb)-1)
    Fb.clear()
    Fin_Bin = Fin_Bin.split(b"/:>\r\n")
    Write_Binary = open(str(Fin_Bin[0]).replace("\\\\", "\\").replace("b'", "").replace("'", ""), "wb")
    Write_Binary.write(Fin_Bin[1])
    Write_Binary.close()