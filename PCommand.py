import BF_ObjectDef as OB

def DispPlayerStatus(Player, Flag):
    strval_1 = Player.Equips["Weapon"]
    strval_2 = Player.Equips["Armor"]
    strval_3 = Player.Equips["Accesory"]
    PS = str(Player.Status)[1:-1]
    #AS = str(Player.Accesory.instatus)[1:-1]
    if Player.STR > 0:
        STR = "STR:" + str(Player.STR) + " "
    else:
        STR = ""
    if Player.INT > 0:
        INT = "INT:" + str(Player.INT) + " "
    else:
        INT = ""
    if Player.VIT > 0:
        VIT = "VIT:" + str(Player.VIT) + " "
    else:
        VIT = ""
    if (Player.MGR - Player.Armor.MGR) > 0:
        MGR = "MGR:" + str(Player.MGR - Player.Armor.MGR) + " "
    else:
        MGR = ""
    if Player.Atk3 > 0:
        Atk3val = "+" + str(Player.Atk3)
    else:
        Atk3val = ""
    if Player.Armor.def2 > 0:
        def2val = "+" + str(Player.Armor.def2)
    else:
        def2val = ""
    if Player.Weapon.slot > 0:
        WepinstatusVal = Player.Weapon.instatus
    else:
        WepinstatusVal = ""
    if Player.Armor.slot > 0:
        ArminstatusVal = Player.Armor.instatus
    else:
        ArminstatusVal = ""
    if Player.Accesory.slot > 0:
        AccinstatusVal = Player.Accesory.instatus
    else:
        AccinstatusVal = ""
    Skills = f"{STR}{INT}{VIT}{MGR}{PS}"
    if Skills == "":
        Skills = "none"
    #print(f"  <{Player.name} Lv{Player.Lv} : {Player.HP} / {Player.MP}> {STR}{INT}{VIT}{MGR}{PS}")
    #print(f"    *{strval_1} : {Player.Atk1}d{Player.Atk2}{Atk3val} {WepinstatusVal} *{strval_2} : {Player.Armor.def1}{def2val},{Player.MGR} {ArminstatusVal} *{strval_3} : {AccinstatusVal} {Player.gold}gold")
    if Flag == True:
        t0 = f"{Player.name} : {Player.HP} / {Player.MP} {Player.gold}gold  \n"
    else:
        t0 = ""
    t1 = f"Skills : {Skills}"
    t2 = f"*{strval_1} : {Player.Atk1}d{Player.Atk2}{Atk3val} {WepinstatusVal}"
    t3 = f"*{strval_2} : {Player.Armor.def1}{def2val},{Player.MGR} {ArminstatusVal}"
    t4 = f"*{strval_3} : {AccinstatusVal}"
    return (t0 + t1 + "  \n" + t2 + "  \n" + t3 + "  \n" + t4)

def DispEnemyStatus(Enemy, Flag):
    if Enemy.STR > 0:
        STR = "STR:" + str(Enemy.STR) + " "
    else:
        STR = ""
    if Enemy.INT > 0:
        INT = "INT:" + str(Enemy.INT) + " "
    else:
        INT = ""
    if Enemy.VIT > 0:
        VIT = "VIT:" + str(Enemy.VIT) + " "
    else:
        VIT = ""
    if Enemy.MGR > 0:
        MGR = "MGR:" + str(Enemy.MGR) + " "
    else:
        MGR = ""
    if Enemy.Atk3 > 0:
        Atk3val = "+" + str(Enemy.Atk3)
    else:
        Atk3val = ""
    PS = str(Enemy.Status)[1:-1]
    Skills = f"{STR}{INT}{VIT}{MGR}{PS}"
    if Skills == "":
        Skills = "none"
    #print(f"  <{Enemy.name} : {Enemy.HP} / {Enemy.MP}> {STR}{INT}{VIT}{MGR}{PS}")
    #print(f"    *Weapon : {Enemy.Atk1}d{Enemy.Atk2} {Atk3val} *Armor : {Enemy.Def},{Enemy.MGR}")
    if Flag == True:
        t0 = f"{Enemy.name} {Enemy.HP} / {Enemy.MP}  \n"
    else:
        t0 = ""
    t2 = f"Skills : {Skills}"
    t3 = f"*Weapon : {Enemy.Atk1}d{Enemy.Atk2} {Atk3val}"
    t4 = f"*Armor : {Enemy.Def},{Enemy.MGR}"
    #return (t0 + t2 + "  \n" + t3 + "  \n" + t4 + "  \n" + "*none")
    return (t0 + t2 + "  \n" + t3 + "  \n" + t4)

def DispResult(Player, Enemy):
    if Player.HP < 1:
        Player.HP = 0
    if Enemy.HP < 1:
        Enemy.HP = 0
    print(f"  *{Player.name}: {Player.HP} / {Player.MP}")
    print(f"  *{Enemy.name}: {Enemy.HP} / {Enemy.MP}")

def DispWeaponStatus(txt, Weapon, name):
    if Weapon.Atk3 > 0:
        W3val = "+" + str(Weapon.Atk3)
    else:
        W3val = ""
    if Weapon.slot > 0:
        WI = Weapon.instatus
    else:
        WI = ""
    t1 = txt + f"{name}:{Weapon.Atk1}d{Weapon.Atk2} {W3val} {WI}"
    return t1

def DispArmorStatus(txt, Armor, name):
    if Armor.slot > 0:
        AI = Armor.instatus
    else:
        AI = ""
    t1 = txt + f"{name}:{Armor.def1},{Armor.MGR} {AI}"
    return t1

def DispAccesoryStatus(Player):
    CS = Player.Equips["Accesory"]
    print(f"{CS} {Player.Accesory.instatus}")

def SelectWeapon(Player, NewWeapon):
        text = "You get a Weapon!"
        DispWeaponStatus("New:",NewWeapon, NewWeapon.name)
        #NowEquipsName = Player.Equips["Weapon"]
        DispWeaponStatus("Now:",Player.Weapon, Player.Equips["Weapon"])
        print("Exchange? y/n:")
        getch = Script._Getch()
        n = getch()
        if n == b'y':
            print(f"Equip a new {NewWeapon.name}!")
            Player.Equip(NewWeapon, Player.Armor, Player.Accesory)   
            return "y"
        return "n"

def MakeGetWeapon(cnt, Player):
    Sel = OB.DiceRoll(1,1200)
    if  Sel == 1:
        NewWeapon = OB.WeaponStatus("MurasameBlade!", int((cnt+2)), 10, 0, 1, "", ["INT25"])
    elif Sel == 2:
        NewWeapon = OB.WeaponStatus("Shurikens!", 1, (cnt+4) * 10, 0, 1, "", ["VIT20"])
    elif Sel == 3:
        NewWeapon = OB.WeaponStatus("Exculliber!", OB.DiceRoll(1, ((cnt+8)//3)+2), OB.DiceRoll(2, cnt+6+6), 0, 2, "", ["INT25", "MGR25"])
    else:
        Atk1 = OB.DiceRoll(1, (cnt//3)+2)
        Atk2 = OB.DiceRoll(1, cnt+6)
        Score = int(Atk1 * Atk2)
        if Score > 180:
            name = "BasterdSword"
        elif Score > 140:
            name = "GreatSword"
        elif Score > 100:
            name = "BloadSword"
        elif Score > 60:
            name = "LongSword"
        elif Score > 19:
            name = "ShortSword"
        else:
            name = "Dagger"
        NewWeapon = OB.WeaponStatus(name, Atk1, Atk2, 0, 0, "", [])
    return NewWeapon

def GetWeapon(cnt, Player):
    NewWeapon = MakeGetWeapon(cnt, Player)
    return NewWeapon
    if NewWeapon.score > Player.Weapon.score * 0.95:
        SelectWeapon(Player, NewWeapon)
    else:
        return

def SelectArmor(Player, NewArmor):
        print("You get a Armor!")
        DispArmorStatus("New:", NewArmor, NewArmor.name)
        DispArmorStatus("Now:", Player.Armor, Player.Equips["Armor"])
        print("Exchange? y/n:")
        getch = Script._Getch()
        n = getch()
        if n == b'y':
            print(f"Equip a new {NewArmor.name}!")
            Player.Equip(Player.Weapon, NewArmor, Player.Accesory)
            return "y"
        return "n"

def MakeGetArmor(cnt, Player):
    Sel = OB.DiceRoll(1,1200)
    if Sel == 1:
        NewArmor = OB.ArmorStatus("BattleSuite!", int((cnt+6)*(Player.Lv*1.6)), 0, 1, "", ["VIT20"])
    elif Sel == 2:
        NewArmor = OB.ArmorStatus("O-GUSOKU!", int((cnt+6)*(Player.Lv*2)), 25, 1, "", ["STR25"])
    elif Sel == 3:
        NewArmor = OB.ArmorStatus("GoldCloss!",OB.DiceRoll(((cnt+8)//4)+1, cnt+2+8), 25, 2, "", ["STR25","INT25"])
    else:
        defv = OB.DiceRoll((cnt//4)+1, cnt+2)
        MGR = OB.DiceRoll(1,25)
        if defv > 120:
            name = "FullPlateArmor"
        elif defv > 96:
            name = "PlateArmor"
        elif defv > 64:
            name = "ScaleArmor"
        elif defv > 32:
            name = "ChainArmor"
        elif defv > 12:
            name = "LeatherArmor"
        else:
            name = "Cloth"
        NewArmor = OB.ArmorStatus(name, defv, MGR, 0, "", [])
    return NewArmor

def GetArmor(cnt, Player):
    NewArmor = MakeGetArmor(cnt, Player)
    return NewArmor
    #if NewArmor.score > Player.Armor.score * 0.9:
    #    SelectArmor(Player, NewArmor)

def SelectScroll(Player, NewScroll):
    print(f"*** You Get a {NewScroll.name}! ***")
    while True:
        print("w:Enchant Weapon a:Enchant Armor c:Enchant Accesory d:Drop")
        getch = Script._Getch()
        n = getch()
        if n == b'w':
            print(f"Enchant Weapon with {NewScroll.status}")
            Player.Weapon.AddStatus(NewScroll.status)
            Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
            return "y"
        elif n == b'a':
            print(f"Enchant Armor with {NewScroll.status}")
            Player.Armor.AddStatus(NewScroll.status)
            Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
            return "y"
        elif n == b'c':
            Player.Accesory.AddStatus(NewScroll.status)
            Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
            return "y"
        elif n == b'd':
            print("Dropped Scroll.")
            return "n"
        else:
            print("Invalid Command!")

def MakeGetScroll(StageStr, Sel):
    if Sel < 2:
        Sta = "Swings"
    elif Sel < 3:
        Sta = "Aura"
    elif Sel < 4:
        Sta = "Curse"
    elif Sel < 6:
        Sta = "Critical"
    elif Sel < 8:
        Sta = "Power"
    elif Sel < 10:
        Sta = "Fire"
    elif Sel < 14:
        Sta = "Mana"
    elif Sel < 19:
        Sta = "Heal"
    else:
        Sta = "none"
    NewScroll = OB.ScrollStatus(Sta)
    return NewScroll

def GetScroll(Player, Rew, StageStr):
    if StageStr == "Abyss":
        det = 300 - int(Rew * 25)
    elif StageStr == "EvilCastle":
        det = 350 - int(Rew * 25)
    else:
        det = 400 - int(Rew * 25)
    Sel = OB.DiceRoll(1, det)
    NewScroll = MakeGetScroll(StageStr, Sel)
    return NewScroll
    #SelectScroll(Player, NewScroll)

def SelectCrystal(Player, NewCrystal):
    print(f"*** You Get a {NewCrystal.name}! ***")
    while True:
        if Player.Weapon.slot > 0:
            if Player.Armor.slot > 0:
                print("w:Enchant Weapon a:EnchantArmor c:Enchant Accesory d:Drop")
            else:
                print("w:Enchant Weapon c:Enchant Accesory d:Drop")
        else:
            print("c:Enchant Accesory d:Drop")
        getch = Script._Getch()
        n = getch()
        if n == b'c':
            DispAccesoryStatus(Player)
            print("Select Accesory's slot.")
            getch = Script._Getch()
            n = getch()
            try:
                Num = int(n.decode())
            except:
                Num = 99
            if Num < Player.Accesory.slot+1 and str.isdecimal(str(Num)):
                print("Enchant Accesory!")
                Player.Accesory.AddInstatus(Num, NewCrystal.status)
                Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
                return "y"
            else:
                print("Invalid select!")
        elif n == b'w':
            #DispWeaponStatus("Now", Player.Weapon, Player.Equips["Weapon"])
            print("Select Weapon's slot.")
            getch = Script._Getch()
            n = getch()
            try:
                Num = int(n.decode())
            except:
                Num = 99
            if Num < Player.Weapon.slot+1 and str.isdecimal(str(Num)):
                print("Enchant Weapon!")
                Player.Weapon.AddInstatus(Num, NewCrystal.status)
                Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
                return "y"
            else:
                print("Invalid select!")            
        elif n == b'a':
            #DispArmorStatus("Now", Player.Armor, Player.Equips["Armor"])
            print("Select Armor's slot.")
            getch = Script._Getch()
            n = getch()
            try:
                Num = int(n.decode())
            except:
                Num = 99
            if Num < Player.Armor.slot+1 and str.isdecimal(str(Num)):
                print("Enchant Armor!")
                Player.Armor.AddInstatus(Num, NewCrystal.status)
                Player.Equip(Player.Weapon, Player.Armor, Player.Accesory)
                return "y"
            else:
                print("Invalid select!")                 
        elif n == b'd':
            print("Dropped Scroll.")
            return "n"
        else:
            print("Invalid select!")

def MakeGetCrystal(Player, StageStr, Sel):
    if Sel < 2:
        Sta = "STR"
        Val = OB.DiceRoll(1, Player.Lv * 5)
    elif Sel < 3:
        Sta = "INT"
        Val = OB.DiceRoll(1, Player.Lv * 5)
    elif Sel < 4:
        Sta = "VIT"
        Val = OB.DiceRoll(1, Player.Lv * 4)
    elif Sel < 5:
        Sta = "MGR"
        Val = OB.DiceRoll(1, Player.Lv * 5)
    else:
        Sta = "none"
        Val = 0
    Sta = Sta + str(Val)
    NewCrystal = OB.CrystalStatus(Sta)
    return NewCrystal

def GetCrystal(Player, Rew, StageStr):
    if StageStr == "Abyss":
        det = 100 - int(Rew * 20)
    elif StageStr == "EvilCastle":
        det = 150 - int(Rew * 20)
    else:
        det = 200 - int(Rew * 20)
    Sel = OB.DiceRoll(1, det)
    NewCrystal = MakeGetCrystal(Player, StageStr, Sel)
    return NewCrystal
    #SelectCrystal(Player, NewCrystal)

def GetShopItem(MonRew, Rew, Player, StageStr):
    if StageStr == "Abyss":
        det = 100 - (MonRew * 12)
    elif StageStr == "EvilCastle":
        det = 150 - (MonRew * 12)
    else:
        det = 200 - (MonRew * 12)
    Sel1 = OB.DiceRoll(1,det)
    if Sel1 < 2:
        Sel2 = OB.DiceRoll(1, 18)
        Items = MakeGetScroll(StageStr, Sel2)
    elif Sel1 < 3:
        Sel2 = OB.DiceRoll(1, 4)
        Items = MakeGetCrystal(Player, StageStr, Sel2)
    elif Sel1 < int(det/2):
        Items = MakeGetWeapon(Rew, Player)
    else:
        Items = MakeGetArmor(Rew, Player)
    return Items

def GetItem(Player, Lv):
    Sel = OB.DiceRoll(1,20)
    if Sel > 11:
        print(f"You get a HitPotion!")
        Player.Battle_Healing(0, 2, 6 + Player.Lv, 1, True)
    elif Sel > 3:
        print(f"You get a MagicPotion!")
        Player.Battle_MPing(0, 1, 4 + Player.Lv, 1, True)
    else:
        HPVal = OB.DiceRoll(1,4)
        MPVal = OB.DiceRoll(1,2)
        print("*** You are Power UP! ***")
        print(f"HP {HPVal} UP!")
        print(f"MP {MPVal} UP!")
        Player.LevelUP(HPVal, MPVal)