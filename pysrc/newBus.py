import pandas as pd
import math

def addBus(csvID = 0):	
	busList = pd.read_table("pysrc/all.csv", sep = ',')
	Name = busList.at[csvID,"Name"]
	spriteList = pd.read_table("pysrc/buses/" + Name + ".csv", sep = ',')
	amountSprites = spriteList.shape[0]	
	main = open('jpbus.pnml', 'a')#w overrides, a appends
	main.write("\n#include \"" + "src/buses/" + Name + ".pnml" + "\"")
	main.close()
	length = str(busList.at[csvID,"Length"])
	f = open("src/buses/" + Name + ".pnml", 'w')#w overrides, a appends
	
	#Spritesets
	for i in range(amountSprites):
		f.write("spriteset (SPRITESET_" + Name + "_" + str(i) + ", \"gfx/" + spriteList.at[i,"File"] + "\") {\n" +
		"	template_2cc_" + length + "8(1," + str(1+26*spriteList.at[i,"y"]) + ")\n" +
		"}\n")
		if (spriteList.at[i,"32bpp"] == 1):
			f.write("alternative_sprites (SPRITESET_" + Name + "_" + str(i) + ", ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, \"gfx/" + spriteList.at[i,"32bppFile"] + "\") {\n" +
			"	template_2cc_" + length + "8(1," + str(1+26*spriteList.at[i,"y"]) + ")\n" +
			"}\n")
	
	#Random switch
	f.write("random_switch(FEAT_ROADVEHS, PARENT, switch_random_" + Name + ") {\n")
	for i in range(amountSprites):
		f.write("	" + str(spriteList.at[i,"Weight"]) + ": SPRITESET_" + Name + "_" + str(i) + ";\n")
	f.write("}\n")

	#Livery sprites
	f.write("switch(FEAT_ROADVEHS,SELF,switch_" + Name + "_GFX,cargo_subtype){\n" +
	"    0: 	switch_random_" + Name + ";\n")
	for i in range(amountSprites):
		f.write("	" + str(i+1) + ":	SPRITESET_" + Name + "_" + str(i) + ";\n")
	f.write("}\n")
	
	#Livery sprites
	f.write("switch(FEAT_ROADVEHS,SELF,switch_" + Name + "_livery,cargo_subtype){\n" +
	"    0: 	return string(STR_LIV_DEFAULT);\n")
	for i in range(amountSprites):
		f.write("	" + str(i+1) + ":	return string(" + spriteList.at[i,"Livery"] + ");\n")
	f.write("		return CB_RESULT_NO_TEXT;\n" + 
	"}\n")

	#purchase sprite
	f.write("\nspriteset (SPRITESET_PURCH_" + Name + ", \"gfx/" + busList.at[csvID,"PurchFile"] + "\") {\n" +
	"	template_purchase(" + str(busList.at[csvID,"PurchX"]) + "," + str(busList.at[csvID,"PurchY"]) + ")\n" +
	"}\n")
	if (busList.at[csvID,"32bppPurch"] == 1):
		f.write("\nalternative_sprites (SPRITESET_PURCH_" + Name + ", ZOOM_LEVEL_NORMAL, BIT_DEPTH_32BPP, \"gfx/" + busList.at[csvID,"32bppPurchFile"] + "\") {\n" +
		"	template_purchase(" + str(busList.at[csvID,"PurchX"]) + "," + str(busList.at[csvID,"PurchY"]) + ")\n" +
		"}\n")
	
	f.write("\nitem(FEAT_ROADVEHS, " + Name + ", ITEM_" + Name + ") {\n" +
	"	property {\n" +
	"		sprite_id: SPRITE_ID_NEW_ROADVEH;\n" +
	"		running_cost_base: RUNNING_COST_ROADVEH;\n" +
	"		climates_available: ALL_CLIMATES;\n" +
	"		misc_flags: bitmask(ROADVEH_FLAG_AUTOREFIT);\n" +
	"		road_type: " + busList.at[csvID,"Roadtype"] + ";\n" +
	"		refittable_cargo_classes: bitmask(CC_PASSENGERS);\n" +
	"		default_cargo_type: PASS;\n" +
	"		" + busList.at[csvID,"LoadingSpeed"] + "\n" +
	"		tractive_effort_coefficient: 0.3;\n" +
	"		refit_cost: 0;\n" +
	"		reliability_decay:	12;\n" +
	"		vehicle_life: 50;\n" +
	"		name:	string(" + busList.at[csvID,"STR"] + ");\n" +
	"		speed: " + str(busList.at[csvID,"Speed"]) + " km/h;\n" +
	"		air_drag_coefficient: " + str(busList.at[csvID,"Air"]) + ";\n" +
	"		introduction_date:	date(" + str(busList.at[csvID,"Intro"]) + ",01,01);\n" +
	"		model_life:	VEHICLE_NEVER_EXPIRES;\n" +
	"		cost_factor: " + str(busList.at[csvID,"Purchase"]) + ";\n" +
	"		running_cost_factor: " + str(busList.at[csvID,"Maintenance"]) + ";\n" +
	"		power: " + str(busList.at[csvID,"Power"]) + " kW;\n" +
	"		cargo_capacity: " + str(busList.at[csvID,"Capacity"]) + ";\n" +
	"		weight: " + str(busList.at[csvID,"Mass"]) + " tons;\n" +
	"		length: " + length + ";\n" +
	"	}\n" +
	"	graphics {\n" +
	"		default: switch_" + Name + "_GFX;\n" +
	"		purchase: SPRITESET_PURCH_" + Name + ";\n" +
	"		cargo_subtype_text: switch_" + Name + "_livery;\n" +
	"	}\n" +
	"}\n")
	
	f.close()