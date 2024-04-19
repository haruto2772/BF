import streamlit as st
import BF_stTown as Town
import BF_stBF as stBF
import BF_ObjectDef as OB
import PCommand as PC

def PlayerDef():
    name = st.session_state["inname"]
    if "!3" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 3, 160, 60, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    elif "!4" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 4, 200, 80, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    elif "!5" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 5, 240, 100, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    elif "!6" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 6, 280, 120, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    elif "!7" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 7, 320, 140, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    elif "!8" in name:
        st.session_state["Player"] = OB.PlayerStatus(name, 8, 380, 160, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    else:
        st.session_state["Player"] = OB.PlayerStatus(name, 1, 100, 30, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 20)
    if "Saikyo" in name:
        st.session_state["Player"].LevelUP(9999, 9999)
        st.session_state["Player"].gold = 9999
    if "Aura" in name:
        st.session_state["Player"].Accesory.AddStatus("Aura")
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    elif "Curse" in name:
        st.session_state["Player"].Accesory.AddStatus("Curse")
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory)
    elif "Swings" in name:
        st.session_state["Player"].Accesory.AddStatus("Swings")
        st.session_state["Player"].Equip(st.session_state["Player"].Weapon, st.session_state["Player"].Armor, st.session_state["Player"].Accesory) 
    st.session_state["page_control"] = 0

def change_Town():
    st.session_state["page_control"] = 0

def change_Shop():
    st.session_state["page_control"] = 1

def change_Enchant():
    st.session_state["page_control"] = 2

def change_AddSlot():
    st.session_state["page_control"] = 3

def change_BFinit(BF):
    st.session_state["BF"] = BF
    st.session_state["ShopList"] = []
    st.session_state["page_control"] = 5

def Null_page():
    st.session_state["page_control"] = 999

if("page_control" in st.session_state and st.session_state["page_control"] == 0 ):
    st.session_state["Player"].Reflesh()
    st.session_state["cnt"] = 0
    if st.session_state["Player"].Lv == 1:
        st.session_state["BF1"] = OB.BFStatus("DarkWood", 1, 0, 0)
        st.session_state["BF2"] = OB.BFStatus("none", 1, 0, 0)
    elif st.session_state["Player"].Lv == 2:
        st.session_state["BF1"] = OB.BFStatus("DarkWood", 1, 0, 0)
        st.session_state["BF2"] = OB.BFStatus("DoomsCave", 2, 4, 0)
    elif st.session_state["Player"].Lv == 3:
        st.session_state["BF1"] = OB.BFStatus("DoomsCave", 2, 4, 0)
        st.session_state["BF2"] = OB.BFStatus("RuinFortless", 3, 8, 0)
    elif st.session_state["Player"].Lv == 4:
        st.session_state["BF1"] = OB.BFStatus("RuinFortless", 3, 8, 0)
        st.session_state["BF2"] = OB.BFStatus("EvilCastle", 4, 12, 0)
    elif st.session_state["Player"].Lv == 5:
        st.session_state["BF1"] = OB.BFStatus("EvilCastle", 4, 12, 0)
        st.session_state["BF2"] = OB.BFStatus("Abyss", 5, 16, 0)
    elif st.session_state["Player"].Lv == 6:
        st.session_state["BF1"] = OB.BFStatus("Abyss", 5, 16, 0)
        st.session_state["BF2"] = OB.BFStatus("ChaosePlane", 6.4, 20, 0)
    elif st.session_state["Player"].Lv == 7:
        st.session_state["BF1"] = OB.BFStatus("ChaosePlane", 6.4, 20, 0)
        st.session_state["BF2"] = OB.BFStatus("YAMATO", 7.8, 24, 0)
    elif st.session_state["Player"].Lv > 7:
        st.session_state["BF1"] = OB.BFStatus("YAMATO", 7.8, 24, 0)
        st.session_state["BF2"] = OB.BFStatus("Vhalhara", 10, 30, 0)
    else:
        st.session_state["BF1"] = OB.BFStatus("none", 1, 0, 0)
        st.session_state["BF2"] = OB.BFStatus("none", 1, 0, 0)       
    Town.Town()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 1 ):
    Town.Shop()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 11 ):
    stBF.SelectWeapon()
    st.session_state["page_control"] = 1
elif ("page_control" in st.session_state and st.session_state["page_control"] == 12 ):
    stBF.SelectArmor()
    st.session_state["page_control"] = 1
elif ("page_control" in st.session_state and st.session_state["page_control"] == 13 ):
    stBF.SelectScroll()
    st.session_state["page_control"] = 1
elif ("page_control" in st.session_state and st.session_state["page_control"] == 14 ):
    stBF.SelectCrystal(False)
    st.session_state["page_control"] = 1
elif ("page_control" in st.session_state and st.session_state["page_control"] == 2 ):
    Town.Enchant()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 21 ):
    Town.Enchant_Weapon()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 22 ):
    Town.Enchant_Armor()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 3 ): 
    Town.AddSlot()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 31 ):
    Town.AddSlot_Weapon()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 32 ):
    Town.AddSlot_Armor()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 4 ): 
    Town.ElderAdvice()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 5 ):
    stBF.BFinit()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 51 ):
    stBF.BFResult()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 52 ):
    stBF.GetWeapon()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 53 ):
    stBF.GetArmor()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 54 ):
    stBF.GetScroll()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 55 ):
    stBF.GetCrystal()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 551 ):
    stBF.Crystal_Weapon(5)
elif ("page_control" in st.session_state and st.session_state["page_control"] == 552 ):
    stBF.Crystal_Armor(5)
elif ("page_control" in st.session_state and st.session_state["page_control"] == 553 ):
    stBF.Crystal_Accesory(5) 
elif ("page_control" in st.session_state and st.session_state["page_control"] == 554 ):
    stBF.Crystal_Weapon(1)
elif ("page_control" in st.session_state and st.session_state["page_control"] == 555 ):
    stBF.Crystal_Armor(1)
elif ("page_control" in st.session_state and st.session_state["page_control"] == 556 ):
    stBF.Crystal_Accesory(1) 
elif ("page_control" in st.session_state and st.session_state["page_control"] == 57 ):
    stBF.BFResult_PlayerWin()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 58 ):
    stBF.BFResult_PlayerLose()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 59 ):
    stBF.BF_MANUAL_skill()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 6 ):
    Town.Ending01()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 61 ):
    Town.Ending02()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 62 ):
    Town.Ending03()
elif ("page_control" in st.session_state and st.session_state["page_control"] == 999 ):
    st.write("error")
else:
    name = st.text_input('Input Name', key = "inname", on_change = PlayerDef)
    st.session_state["ShopList"] = []

