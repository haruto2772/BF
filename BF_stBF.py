import streamlit as st
import BF_ObjectDef as OB
import PCommand as PC
import BF_stMain as stMain 

def change_BFBattleEnd():
    Item = PC.GetShopItem(st.session_state["Enemy"].Enemy.Rew, \
                          st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew + st.session_state["BF"].cnt, \
                          st.session_state["Player"], st.session_state["BF"].StageName)
    st.session_state["ShopList"].append(Item)
    st.session_state["page_control"] = 52

def change_Deadend():
    #st.session_state["Player"].StatusInit()
    st.session_state["page_control"] = 0      

def LevelUP():
    if st.session_state["Player"].Lv == 4:
        HPVal = 1
    elif st.session_state["Player"].Lv > 4:
        HPVal = 2
    else:
        HPVal = 0
    LV1 = OB.DiceRoll(1, 4 + HPVal)
    LV2 = OB.DiceRoll(1, 2)
    st.session_state["Player"].LevelUP(LV1, LV2)
    return f"Level Up! HP +{LV1}, MP +{LV2}"

def dropchicket():
    text = ""
    if st.session_state["Enemy"].Enemy.gacha2 != 0:
        Sel = OB.DiceRoll(1,10)
        if Sel < st.session_state["Enemy"].Enemy.gacha2:
            st.session_state["Player"].gacha2 += 1
            text = "You get 1 Premium chicket!!  \n"
        else:
            if st.session_state["Enemy"].Enemy.gacha1 != 0:
                Sel = OB.DiceRoll(1,10)
                if Sel < (st.session_state["Enemy"].Enemy.gacha1 + 1):
                    st.session_state["Player"].gacha1 += 1
                    text = "You get 1 Normal chicket!  \n"            
    else:
        st.session_state["Enemy"].Enemy.gacha1 != 0
        Sel = OB.DiceRoll(1,10)
        if Sel < (st.session_state["Enemy"].Enemy.gacha1 + 1):
            st.session_state["Player"].gacha1 += 1
            text = "You get 1 Normal chicket!  \n"    

    return text       

def BattleResult(text1):
    if st.session_state["Enemy"].Enemy.HP < 1:
        #Enemy Dead
        Enemyname = st.session_state["Enemy"].Enemy.name
        text2 = f"{Enemyname} is Dead!!"
        text2 = f"**:red[{text2}]**"
        text3 = ""
        gold = st.session_state["Enemy"].Enemy.gold
        st.session_state["Player"].gold += gold
        text4 = f"Get {gold} gold."
        #text5 = dropchicket()
        text5 = ""
        Sel = OB.DiceRoll(1,5)
        if Sel == 5:
            text6 = LevelUP()
        else:
            text6 = ""
        if "Immortal!!" in st.session_state["Player"].Status:
            text7 = st.session_state["Player"].Battle_Healing(0, st.session_state["Player"].Lv, 10, 1, True)
            text8 = st.session_state["Player"].Battle_MPing(0, 2, st.session_state["Player"].Lv + 1, 1, True)
        else:
            if "Heal" in st.session_state["Player"].Status:
                text7 = st.session_state["Player"].Battle_Healing(0, st.session_state["Player"].Lv, 6, 1, True)
            else:
                text7 = ""
            if "Mana" in st.session_state["Player"].Status:
                text8 = st.session_state["Player"].Battle_MPing(0, 1, st.session_state["Player"].Lv + 1, 1, True)
            else:
                text8 = ""
        if text7 != "" or text8 != "":
            text6 += "  \n"
        if text8 != "":
            text7 += "  \n"
        st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3 + "  \n" + text4 + "  \n" + text5 + "  \n" + text6 + text7 + text8
        st.session_state["page_control"] = 57
    else:
        text2 = st.session_state["Enemy"].Enemy_Attack(st.session_state["Player"], st.session_state.AuraFlag)
        if "Aura" in text2:
            st.session_state.AuraFlag = False
        if st.session_state["Player"].HP < 1:
            #Player Dead
            name = st.session_state["Player"].name
            text3 = f"*** {name} is Dead!! ***"
            text3 = f"**:red[{text3}]**"
            st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3
            st.session_state["page_control"] = 58
        else:
            #Battle Continue
            text3 = ""
            st.session_state["BFResult"] = text1 + "  \n" + text2 + "  \n" + text3
            st.session_state["page_control"] = 51

def BF_Attack():
    text1 = ""; text2 = "";text3 = "";
    if "Slash!!" in st.session_state["Player"].Status and "Swings!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 0, 4, False)
    elif "Slash!!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 0, 3, False)
    elif "Swings!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 0, 2, False)
    else:
        text1 = st.session_state["Player"].Battle_Attack(st.session_state["Enemy"].Enemy, False)
    if "Fire" in st.session_state["Player"].Status:
        text2 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv, False) 
    else:
        text2 = ""
    if "Inferno!!" in st.session_state["Player"].Status:
        text3 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv * 3, True) 
    else:
        text3 = ""
    if "Curse!" in st.session_state["Player"].Status:
        text4 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 0, 1, 4, 1, 4, st.session_state["Player"].Lv)
    else:
        text4 = ""
    if text2 != "" or text3 != "" or text4 != "":
        text1 += "  \n"
    if text3 != "" or text4 != "":
        text2 += "  \n"
    if text4 != "":
        text3 += "  \n"
    BattleResult(text1 + text2 + text3 + text4)

def BF_WAttack():
    text1 = ""; text2 = "";text3 = "";
    if "Slash!!" in st.session_state["Player"].Status and "Swings!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 4, 5, False)
    elif "Slash!!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 4, 4, False)
    elif "Swings!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 4, 3, False)
    else:
        text1 = st.session_state["Player"].Battle_MultiAttack(st.session_state["Enemy"].Enemy, 4, 2, False)
    if "Fire" in st.session_state["Player"].Status:
        text2 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv,False) 
    else:
        text2 = ""
    if "Inferno!!" in st.session_state["Player"].Status:
        text3 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 0, 2, 12, st.session_state["Player"].Lv * 3, True) 
    else:
        text3 = ""
    if "Curse!" in st.session_state["Player"].Status:
        text4 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 0, 1, 4, 1, 4, st.session_state["Player"].Lv)
    else:
        text4 = ""
    if text2 != "" or text3 != "" or text4 != "":
        text1 += "  \n"
    if text3 != "" or text4 != "":
        text2 += "  \n"
    if text4 != "":
        text3 += "  \n"
    BattleResult(text1 + text2 + text3 + text4)

def BF_Healing():
    text1 = st.session_state["Player"].Battle_Healing(6, 3, 16, st.session_state["Player"].Lv, False)
    BattleResult(text1)

def BF_FireBall():
    if "Inferno!!" in st.session_state["Player"].Status:
        text1 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 8, 3, 16, st.session_state["Player"].Lv * 3, True)
    else:
        text1 = st.session_state["Player"].Battle_FireBall(st.session_state["Enemy"].Enemy, 8, 3, 16, st.session_state["Player"].Lv, False)
    BattleResult(text1)

def BF_Curse():
    text1 = st.session_state["Player"].Battle_Curse(st.session_state["Enemy"].Enemy, 12, 2, 4, 2, 4, st.session_state["Player"].Lv)
    BattleResult(text1)

def BF_Barrier():
    text1 = st.session_state["Player"].Battle_Barrier(5, 30)
    BattleResult(text1)

def DispBFinfo():
    Stage = st.session_state["BF"].StageName
    cnt = st.session_state["BF"].cnt
    st.subheader(f"Stage: {Stage} <{cnt}>")

def BF_MANUAL():
    st.session_state["page_control"] = 59

def BF_MANUAL_skill():
    DispBattleHP()
    DispPlayerComand2()
    Manual_SKill()

def BFResult():
    #DispBFinfo()
    #stMain.DispEStatus()
    #BF_DispPlayerComand()
    DispBattleHP()
    DispPlayerComand2()
    st.write(st.session_state["BFResult"])

def BFResult_PlayerWin():
    #DispBFinfo()
    #stMain.DispEStatus()
    #BF_DispPlayerStatus()
    DispBattleHP()
    #DispPlayerComand2()
    st.divider()
    st.markdown(st.session_state["BFResult"]) 
    st.button("--------- OK ----------", key = "OK_BF01", on_click = change_BFBattleEnd)   

def BFResult_PlayerLose():
    #DispBFinfo()
    #stMain.DispEStatus()
    #BF_DispPlayerStatus()
    DispBattleHP()
    #DispPlayerComand2()
    st.divider()
    st.markdown(st.session_state["BFResult"]) 
    st.button("--------- OK ----------", key = "OK_BF01", on_click = change_Deadend)      

#
def BF_DispPlayerStatus():
    st.header("BF 1.3b")
    text = PC.DispPlayerStatus(st.session_state["Player"], True)
    st.markdown(text)

def DispBattleHP():
    DispBFinfo()
    text1 = PC.DispEnemyStatus(st.session_state["Enemy"].Enemy, False)
    text2 = PC.DispPlayerStatus(st.session_state["Player"], False)
    Pname = st.session_state["Player"].name
    if st.session_state["Player"].HP < (st.session_state["Player"].MaxHP / 5):
        PHP = st.session_state["Player"].HP
        PHP = f":red[{PHP}]"
        PMP = st.session_state["Player"].MP
    else:
        PHP = st.session_state["Player"].HP
        PMP = st.session_state["Player"].MP
    Ename = st.session_state["Enemy"].Enemy.name
    if st.session_state["Enemy"].Enemy.HP < (st.session_state["Enemy"].Enemy.MaxHP / 5):
        EHP = st.session_state["Enemy"].Enemy.HP
        EHP = f":red[{EHP}]"
        EMP = st.session_state["Enemy"].Enemy.MP
    else:
        EHP = st.session_state["Enemy"].Enemy.HP
        EMP = st.session_state["Enemy"].Enemy.MP
    col5, col6= st.columns([1,1])
    with col5:
        st.markdown(f"#### {Pname} : {PHP} / {PMP} ####")
        st.markdown(text2) 
    with col6:
        st.markdown(f"#### {Ename} : {EHP} / {EMP} ####") 
        st.markdown(text1)

def DispPlayerComand2():   
    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        st.button("----- Attack -----", on_click = BF_Attack)
        if "Inferno!!" in st.session_state["Player"].Status:
            st.button("--- Inferno!!(8) ---", on_click = BF_FireBall)
        else:
            st.button("--- FireBall(8) ---", on_click = BF_FireBall)
    with col2:
        st.button("--- WAttack(4) ---", on_click = BF_WAttack)
        st.button("--- Curse(12)---", on_click = BF_Curse)  
    with col3:
        st.button("--- Healing(6) ---", on_click = BF_Healing)
        st.button(" MANUAL ", on_click = BF_MANUAL)
    with col4:
        st.button("--- Barrier(5) ---", on_click = BF_Barrier)
        st.button("----- Escape -----", on_click = stMain.change_Town)
    st.divider()

def BFinit():
    st.session_state["BF"].cnt += 1
    st.session_state.AuraFlag = True
    st.session_state["Player"].CalcBattleStatus()
    #BF_DispPlayerComand()
    if st.session_state["BF"].cnt > 10:
        SName = st.session_state["BF"].StageName
        text = ""
        if st.session_state["Player"].Lv == 1 and st.session_state["BF"].StageName == "DarkWood" or \
            st.session_state["Player"].Lv == 2 and st.session_state["BF"].StageName == "DoomsCave" or \
            st.session_state["Player"].Lv == 3 and st.session_state["BF"].StageName == "RuinFortless" or \
            st.session_state["Player"].Lv == 4 and st.session_state["BF"].StageName == "EvilCastle" or \
            st.session_state["Player"].Lv == 5 and st.session_state["BF"].StageName == "Abyss" or \
            st.session_state["Player"].Lv == 6 and st.session_state["BF"].StageName == "ChaosePlane" or \
            st.session_state["Player"].Lv == 7 and st.session_state["BF"].StageName == "YAMATO" or \
            st.session_state["Player"].Lv == 8 and st.session_state["BF"].StageName == "Vhalhara":
            if st.session_state["BF"].StageName == "Abyss":
                text = "Conglaturations!! "
            elif st.session_state["BF"].StageName == "Vhalhara":
                text = "Special Conglaturations!! "
            st.session_state["Player"].Lv += 1
            st.subheader(f"** {text}Clear the {SName} **")
            
            getgold = int(OB.DiceRoll(12,20) * st.session_state["BF"].Mag)
            st.session_state["Player"].gold += getgold
            if st.session_state["Player"].Lv < 6:
                st.write("Accesory Slot +1!") 
                st.session_state["Player"].Accesory.AddSlot()   
            st.write(f"Get {getgold} gold!") 
            #st.session_state["Player"].gacha2 += 1
            #st.write("You get 1 Premium chicket!!")
        else:
            st.write(f"Clear the {SName}")
        st.button("Return Town", on_click = stMain.change_Town)
    else:
        st.session_state["Enemy"] = OB.EnemyStatus(st.session_state["BF"].StageName, st.session_state["BF"].Mag, st.session_state["BF"].cnt)
        #stMain.DispEStatus()
        #DispBFinfo()
        EnemyName = st.session_state["Enemy"].Enemy.name
        #DispBattleHP()
        DispBattleHP()
        DispPlayerComand2()
        st.write(f"{EnemyName} is appeared!!")

def Manual_SKill():
    st.write("<Battle Command>  \n")
    st.write("(X)のMPを消費し、特殊な行動をとる \n")
    st.write("Attack   : 武器攻撃。2d6+2は6面ダイス2個分の値+2のダメージ。  \n")  
    st.write("WAttack  : 2回武器攻撃  \n") 
    st.write("Healing  : HP回復  \n") 
    st.write("Barrier  : MGR（魔法防御）UP  \n") 
    st.write("FireBall : 魔法攻撃  \n") 
    st.write("Curse    : 武器攻撃力、防御力へのデバフ  \n") 
    st.write("Escape   : 撤退し、街へ帰還  \n") 

def Manual_Scroll(newScrollname):
    if "Slash!!" in newScrollname or \
        "Immortal!!" in newScrollname or \
        "ZANTETSU!!" in newScrollname or \
        "Inferno!!" in newScrollname:
        st.write("<★Rare Scroll>  \n") 
        st.write("武器、防具、アクセサリに一つ付加可能。効果は重複しない。 \n")
        st.write("Slash    : 攻撃回数+2。  \n")  
        st.write("Immortal : 被武器ダメージ半減＆戦闘終了後、HP,MPが回復  \n") 
        st.write("ZANTETSU : 武器攻撃時、敵のDefとVITを無視  \n") 
        st.write("Inferno  : FireBallコマンドがInfernoに変化＆武器攻撃時、Infernoを使用  \n") 
    else:
        st.write("<Scroll>  \n") 
        st.write("武器、防具、アクセサリに一つ付加可能。効果は重複しない。 \n")
        st.write("Swings   : 攻撃回数+1。  \n")  
        st.write("Aura     : 敵の最初の武器攻撃を無効。以降、10%で敵の武器攻撃を無効。  \n") 
        st.write("Curse    : 武器攻撃時、Curseを使用  \n") 
        st.write("Fire     : 武器攻撃時、FireBallを使用  \n") 
        st.write("Power    : 武器ダイスの前値を+2  \n")
        st.write("Critical : 武器攻撃時、25%でクリティカル攻撃（ダメージ2倍）  \n") 
        st.write("Mana     : 戦闘終了時、MPを回復  \n") 
        st.write("Healing  : 戦闘終了時、HPを回復  \n") 

def Manual_Crystal():
    st.write("<Crystal>  \n")   
    st.write("武器、防具、アクセサリのslotに付加可能。効果は合算される。 \n")
    st.write("STR      : 武器ダイスの後値をX%UP。  \n") 
    st.write("INT      : 魔法効果（FireBall,Healing,Curse）をX%UP。  \n") 
    st.write("VIT      : 武器ダメージをX%軽減  \n") 
    st.write("MGR      : 魔法効果（FireBall）をX%軽減  \n") 

def DispGetItem(text):
    text = f"#### {text} ####"
    st.markdown(f"{text}")    

def Weapon_change():
    NewWeaponName = st.session_state["NewWeapon"].name
    #st.write(f"Equip a new {NewWeaponName}!")
    st.session_state["Player"].Equip(st.session_state["NewWeapon"], st.session_state["Player"].Armor, st.session_state["Player"].Accesory)   
    #st.session_state["page_control"] = 53

def Drop_Weapon():
    pass
    #st.write("Drop Weapon.")
    #st.session_state["page_control"] = 53

def Armor_change():
    NewArmorName = st.session_state["NewArmor"].name
    #st.write(f"Equip a new {NewArmorName}!")
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["NewArmor"], st.session_state["Player"].Accesory)   
    #st.session_state["page_control"] = 54

def Drop_Armor():
    pass
    #st.write("Drop Armor.")
    #st.session_state["page_control"] = 54

def Scroll_Weapon(status):
    st.session_state["Player"].Weapon.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Scroll_Armor(status):
    st.session_state["Player"].Armor.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Scroll_Accesory(status):
    st.session_state["Player"].Accesory.AddStatus(status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    #st.session_state["page_control"] = 55

def Drop_Scroll():
    pass
    #st.write("Drop Scroll.")
    #st.session_state["page_control"] = 55

def SelectWeapon():
    BF_DispPlayerStatus() 
    #DispBFinfo()
    DispGetItem("You get a Weapon!")
    text1 = PC.DispWeaponStatus("New ; ", st.session_state["NewWeapon"], st.session_state["NewWeapon"].name)
    text2 = PC.DispWeaponStatus("Now ; ", st.session_state["Player"].Weapon, st.session_state["Player"].Equips["Weapon"])
    st.write(text1)
    st.write(text2)
    st.button("Exchange", key = "ExchangeWeapon", on_click=Weapon_change)
    st.button("Drop", on_click = Drop_Weapon) 

def GetWeapon():
    st.session_state["NewWeapon"] = PC.GetWeapon(st.session_state["BF"].cnt + st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew, st.session_state["Player"])
    if st.session_state["NewWeapon"].score > st.session_state["Player"].Weapon.score * 0.95:
        SelectWeapon()
        st.session_state["page_control"] = 53
    else:
        GetArmor()

def SelectArmor():
    BF_DispPlayerStatus()
    #DispBFinfo()
    DispGetItem("You get a Armor!")
    text3 = PC.DispArmorStatus("New ; ", st.session_state["NewArmor"], st.session_state["NewArmor"].name)
    text4 = PC.DispArmorStatus("Now ; ", st.session_state["Player"].Armor, st.session_state["Player"].Equips["Armor"])
    st.write(text3)
    st.write(text4)
    st.button("Exchange", key = "ExchangeArmor", on_click=Armor_change)
    st.button("Drop", on_click = Drop_Armor)
    
def GetArmor():
    st.session_state["NewArmor"] = PC.GetArmor(st.session_state["BF"].cnt + st.session_state["BF"].Rew + st.session_state["Enemy"].Enemy.Rew, st.session_state["Player"])
    if st.session_state["NewArmor"].score > st.session_state["Player"].Armor.score * 0.95:
        SelectArmor()
        st.session_state["page_control"] = 54
    else:
        GetScroll()

def SelectScroll():
    BF_DispPlayerStatus()
    #DispBFinfo()
    Scrollname = st.session_state["NewScroll"].name
    DispGetItem(f"You get a {Scrollname}!")
    st.button("Enchant Weapon", key = "Enchant Weapon", on_click=Scroll_Weapon, args=[st.session_state["NewScroll"].status])
    st.button("Enchant Armor", key = "Enchant Armor", on_click=Scroll_Armor, args=[st.session_state["NewScroll"].status])
    st.button("Enchant Accesory", key = "Enchant Accesory", on_click=Scroll_Accesory, args=[st.session_state["NewScroll"].status])
    st.button("Drop", on_click = Drop_Scroll)
    Manual_Scroll(Scrollname)

def GetScroll():
    st.session_state["NewScroll"] = PC.GetScroll(st.session_state["Player"], st.session_state["Enemy"].Enemy.Rew, st.session_state["BF"].StageName)
    if st.session_state["NewScroll"].status != "none":
        SelectScroll()
        st.session_state["page_control"] = 55
    else:
        GetCrystal()

def change_Crystal_Weapon(BFFlag):
    if BFFlag == 1:
        st.session_state["page_control"] = 551
    elif BFFlag == 2:
        st.session_state["page_control"] = 554
    elif BFFlag == 3:
        st.session_state["page_control"] = 557

def change_Crystal_Armor(BFFlag):
    if BFFlag == 1:
        st.session_state["page_control"] = 552
    elif BFFlag == 2:
        st.session_state["page_control"] = 555
    elif BFFlag == 3:
        st.session_state["page_control"] = 558

def change_Crystal_Accesory(BFFlag):
    if BFFlag == 1:
        st.session_state["page_control"] = 553
    elif BFFlag == 2:
        st.session_state["page_control"] = 556
    elif BFFlag == 3:
        st.session_state["page_control"] = 559

def Enchant_Crystal_Weapon(x, status):
    st.session_state["Player"].Weapon.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 

def Crystal_Weapon(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Weapon Slot.")
    for x in range(st.session_state["Player"].Weapon.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Weapon, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Enchant_Crystal_Armor(x, status):
    st.session_state["Player"].Armor.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 

def Crystal_Armor(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Armor Slot.")
    for x in range(st.session_state["Player"].Armor.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Armor, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Enchant_Crystal_Accesory(x, status):
    st.session_state["Player"].Accesory.AddInstatus(x, status)
    st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    
def Crystal_Accesory(page_control):
    BF_DispPlayerStatus()
    st.session_state["page_control"] = page_control
    stStr = st.session_state["NewCrystal"].name
    st.write(f"{stStr}")
    st.write("Select Accesory Slot.")
    for x in range(st.session_state["Player"].Accesory.slot):
        st.button(f"Slot{x+1}", key = x+1, on_click = Enchant_Crystal_Accesory, args = [x+1, st.session_state["NewCrystal"].status])
    st.button("Drop")

def Drop_Crystal(BFFlag):
    #st.write("Drop Crystal!")
    if BFFlag == 1:
        st.session_state["page_control"] = 5
    elif BFFlag == 2:
        st.session_state["page_control"] = 1
    elif BFFlag == 3:
        st.session_state["page_control"] = 7

def SelectCrystal(BFFlag):
    BF_DispPlayerStatus()
    #DispBFinfo()
    Crystalname = st.session_state["NewCrystal"].name
    DispGetItem(f"You get a {Crystalname}!")
    if st.session_state["Player"].Weapon.slot > 0:
        if st.session_state["Player"].Armor.slot > 0:
            st.button("Enchant Weapon", key = "Enchant Weapon", on_click=change_Crystal_Weapon, args=[BFFlag])
            st.button("Enchant Armor", key = "Enchant Armor", on_click=change_Crystal_Armor, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
        else:
            st.button("Enchant Weapon", key = "Enchant Weapon", on_click=change_Crystal_Weapon, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
    else:
        if st.session_state["Player"].Armor.slot > 0:
            st.button("Enchant Armor", key = "Enchant Armor", on_click=change_Crystal_Armor, args=[BFFlag])
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
        else:
            st.button("Enchant Accesory", key = "Enchant Accesory", on_click=change_Crystal_Accesory, args=[BFFlag])
    st.button("Drop", on_click = Drop_Crystal, args=[BFFlag]) 
    Manual_Crystal()  

def GetCrystal():
    st.session_state["NewCrystal"] = PC.GetCrystal(st.session_state["Player"], st.session_state["Enemy"].Enemy.Rew, st.session_state["BF"].StageName)
    if st.session_state["NewCrystal"].status != "none0":
        SelectCrystal(1)      
    else:
        BFinit()

def SelectGoldBag():
    Ggold = st.session_state["NewGold"].gold
    st.write(f"You get {Ggold} gold!")
    st.session_state["Player"].gold += Ggold
    st.button("OK")