\ Begin objective block for master
min 
MASTER:
+1.000000 MASTER_EXPECTED_COST_RootNode

\ End objective block for master

s.t.

\ Begin constraint block for master
MASTER_c_l_Scen2_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen2_StageCost(1)
>= 0.0

MASTER_c_u_Scen2_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen2_StageCost(1)
<= 0.0

MASTER_c_l_Scen3_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen3_Vol(2)
>= 0.0

MASTER_c_u_Scen3_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen3_Vol(2)
<= 0.0

MASTER_c_l_Scen3_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen3_Vol(1)
>= 0.0

MASTER_c_u_Scen3_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen3_Vol(1)
<= 0.0

MASTER_c_l_Scen3_Node3_1_3_StageCost_3_:
+1.000000 MASTER_Node3_1_3_StageCost(3)
-1.000000 Scen3_StageCost(3)
>= 0.0

MASTER_c_u_Scen3_Node3_1_3_StageCost_3_:
+1.000000 MASTER_Node3_1_3_StageCost(3)
-1.000000 Scen3_StageCost(3)
<= 0.0

MASTER_c_l_Scen9_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen9_StageCost(2)
>= 0.0

MASTER_c_u_Scen9_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen9_StageCost(2)
<= 0.0

MASTER_c_l_Scen5_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen5_PDns(2)
>= 0.0

MASTER_c_u_Scen5_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen5_PDns(2)
<= 0.0

MASTER_c_l_Scen5_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen5_PDns(1)
>= 0.0

MASTER_c_u_Scen5_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen5_PDns(1)
<= 0.0

MASTER_c_l_Scen8_Node3_3_2_StageCost_3_:
+1.000000 MASTER_Node3_3_2_StageCost(3)
-1.000000 Scen8_StageCost(3)
>= 0.0

MASTER_c_u_Scen8_Node3_3_2_StageCost_3_:
+1.000000 MASTER_Node3_3_2_StageCost(3)
-1.000000 Scen8_StageCost(3)
<= 0.0

MASTER_c_l_Scen8_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen8_Pgh(2)
>= 0.0

MASTER_c_u_Scen8_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen8_Pgh(2)
<= 0.0

MASTER_c_l_Scen8_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen8_Pgh(1)
>= 0.0

MASTER_c_u_Scen8_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen8_Pgh(1)
<= 0.0

MASTER_c_l_Scen5_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen5_StageCost(1)
>= 0.0

MASTER_c_u_Scen5_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen5_StageCost(1)
<= 0.0

MASTER_c_l_COST_Node2_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_1
-0.333000 MASTER_EXPECTED_COST_Node3_1_1
-0.333000 MASTER_EXPECTED_COST_Node3_1_2
-0.334000 MASTER_EXPECTED_COST_Node3_1_3
-1.000000 MASTER_Node2_1_StageCost(2)
>= 0.0

MASTER_c_u_COST_Node2_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_1
-0.333000 MASTER_EXPECTED_COST_Node3_1_1
-0.333000 MASTER_EXPECTED_COST_Node3_1_2
-0.334000 MASTER_EXPECTED_COST_Node3_1_3
-1.000000 MASTER_Node2_1_StageCost(2)
<= 0.0

MASTER_c_l_Scen4_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen4_Pgt(2)
>= 0.0

MASTER_c_u_Scen4_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen4_Pgt(2)
<= 0.0

MASTER_c_l_Scen4_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen4_Pgt(1)
>= 0.0

MASTER_c_u_Scen4_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen4_Pgt(1)
<= 0.0

MASTER_c_l_Scen2_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen2_Pgh(1)
>= 0.0

MASTER_c_u_Scen2_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen2_Pgh(1)
<= 0.0

MASTER_c_l_Scen2_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen2_Pgh(2)
>= 0.0

MASTER_c_u_Scen2_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen2_Pgh(2)
<= 0.0

MASTER_c_l_Scen7_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen7_PDns(1)
>= 0.0

MASTER_c_u_Scen7_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen7_PDns(1)
<= 0.0

MASTER_c_l_Scen7_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen7_PDns(2)
>= 0.0

MASTER_c_u_Scen7_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen7_PDns(2)
<= 0.0

MASTER_c_l_Scen5_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen5_Pgt(2)
>= 0.0

MASTER_c_u_Scen5_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen5_Pgt(2)
<= 0.0

MASTER_c_l_Scen5_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen5_Pgt(1)
>= 0.0

MASTER_c_u_Scen5_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen5_Pgt(1)
<= 0.0

MASTER_c_l_Scen1_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen1_StageCost(1)
>= 0.0

MASTER_c_u_Scen1_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen1_StageCost(1)
<= 0.0

MASTER_c_l_Scen8_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen8_PDns(1)
>= 0.0

MASTER_c_u_Scen8_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen8_PDns(1)
<= 0.0

MASTER_c_l_Scen8_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen8_PDns(2)
>= 0.0

MASTER_c_u_Scen8_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen8_PDns(2)
<= 0.0

MASTER_c_l_COST_Node3_2_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_3
-1.000000 MASTER_Node3_2_3_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_2_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_3
-1.000000 MASTER_Node3_2_3_StageCost(3)
<= 0.0

MASTER_c_l_Scen1_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen1_StageCost(2)
>= 0.0

MASTER_c_u_Scen1_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen1_StageCost(2)
<= 0.0

MASTER_c_l_Scen3_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen3_Pgh(1)
>= 0.0

MASTER_c_u_Scen3_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen3_Pgh(1)
<= 0.0

MASTER_c_l_Scen3_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen3_Pgh(2)
>= 0.0

MASTER_c_u_Scen3_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen3_Pgh(2)
<= 0.0

MASTER_c_l_Scen4_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen4_PDns(1)
>= 0.0

MASTER_c_u_Scen4_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen4_PDns(1)
<= 0.0

MASTER_c_l_Scen4_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen4_PDns(2)
>= 0.0

MASTER_c_u_Scen4_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen4_PDns(2)
<= 0.0

MASTER_c_l_Scen3_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen3_StageCost(1)
>= 0.0

MASTER_c_u_Scen3_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen3_StageCost(1)
<= 0.0

MASTER_c_l_COST_Node3_2_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_2
-1.000000 MASTER_Node3_2_2_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_2_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_2
-1.000000 MASTER_Node3_2_2_StageCost(3)
<= 0.0

MASTER_c_l_Scen2_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen2_PDns(1)
>= 0.0

MASTER_c_u_Scen2_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen2_PDns(1)
<= 0.0

MASTER_c_l_Scen8_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen8_Vol(1)
>= 0.0

MASTER_c_u_Scen8_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen8_Vol(1)
<= 0.0

MASTER_c_l_Scen6_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen6_Vol(2)
>= 0.0

MASTER_c_u_Scen6_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen6_Vol(2)
<= 0.0

MASTER_c_l_Scen6_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen6_Vol(1)
>= 0.0

MASTER_c_u_Scen6_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen6_Vol(1)
<= 0.0

MASTER_c_l_Scen8_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen8_Vol(2)
>= 0.0

MASTER_c_u_Scen8_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen8_Vol(2)
<= 0.0

MASTER_c_l_Scen3_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen3_Pgt(1)
>= 0.0

MASTER_c_u_Scen3_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen3_Pgt(1)
<= 0.0

MASTER_c_l_Scen3_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen3_Pgt(2)
>= 0.0

MASTER_c_u_Scen3_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen3_Pgt(2)
<= 0.0

MASTER_c_l_COST_Node3_1_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_3
-1.000000 MASTER_Node3_1_3_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_1_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_3
-1.000000 MASTER_Node3_1_3_StageCost(3)
<= 0.0

MASTER_c_l_Scen1_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen1_Vol(1)
>= 0.0

MASTER_c_u_Scen1_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen1_Vol(1)
<= 0.0

MASTER_c_l_Scen1_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen1_Vol(2)
>= 0.0

MASTER_c_u_Scen1_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen1_Vol(2)
<= 0.0

MASTER_c_l_Scen7_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen7_Vol(2)
>= 0.0

MASTER_c_u_Scen7_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen7_Vol(2)
<= 0.0

MASTER_c_l_Scen7_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen7_Vol(1)
>= 0.0

MASTER_c_u_Scen7_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen7_Vol(1)
<= 0.0

MASTER_c_l_Scen6_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen6_StageCost(1)
>= 0.0

MASTER_c_u_Scen6_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen6_StageCost(1)
<= 0.0

MASTER_c_l_COST_Node3_2_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_1
-1.000000 MASTER_Node3_2_1_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_2_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_2_1
-1.000000 MASTER_Node3_2_1_StageCost(3)
<= 0.0

MASTER_c_l_Scen9_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen9_Pgt(2)
>= 0.0

MASTER_c_u_Scen9_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen9_Pgt(2)
<= 0.0

MASTER_c_l_Scen9_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen9_Pgt(1)
>= 0.0

MASTER_c_u_Scen9_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen9_Pgt(1)
<= 0.0

MASTER_c_l_Scen4_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen4_Vol(1)
>= 0.0

MASTER_c_u_Scen4_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen4_Vol(1)
<= 0.0

MASTER_c_l_Scen4_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen4_Vol(2)
>= 0.0

MASTER_c_u_Scen4_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen4_Vol(2)
<= 0.0

MASTER_c_l_COST_Node3_3_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_2
-1.000000 MASTER_Node3_3_2_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_3_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_2
-1.000000 MASTER_Node3_3_2_StageCost(3)
<= 0.0

MASTER_c_l_Scen2_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen2_Pgt(1)
>= 0.0

MASTER_c_u_Scen2_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen2_Pgt(1)
<= 0.0

MASTER_c_l_Scen2_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen2_Pgt(2)
>= 0.0

MASTER_c_u_Scen2_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen2_Pgt(2)
<= 0.0

MASTER_c_l_Scen6_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen6_StageCost(2)
>= 0.0

MASTER_c_u_Scen6_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen6_StageCost(2)
<= 0.0

MASTER_c_l_Scen6_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen6_Pgt(2)
>= 0.0

MASTER_c_u_Scen6_Pgt_2_:
+1.000000 MASTER_Node2_2_Pgt(2)
-1.000000 Scen6_Pgt(2)
<= 0.0

MASTER_c_l_Scen2_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen2_StageCost(2)
>= 0.0

MASTER_c_u_Scen2_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen2_StageCost(2)
<= 0.0

MASTER_c_l_Scen1_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen1_PDns(2)
>= 0.0

MASTER_c_u_Scen1_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen1_PDns(2)
<= 0.0

MASTER_c_l_Scen1_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen1_PDns(1)
>= 0.0

MASTER_c_u_Scen1_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen1_PDns(1)
<= 0.0

MASTER_c_l_COST_Node3_1_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_2
-1.000000 MASTER_Node3_1_2_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_1_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_2
-1.000000 MASTER_Node3_1_2_StageCost(3)
<= 0.0

MASTER_c_l_Scen6_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen6_PDns(2)
>= 0.0

MASTER_c_u_Scen6_PDns_2_:
+1.000000 MASTER_Node2_2_PDns(2)
-1.000000 Scen6_PDns(2)
<= 0.0

MASTER_c_l_Scen6_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen6_PDns(1)
>= 0.0

MASTER_c_u_Scen6_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen6_PDns(1)
<= 0.0

MASTER_c_l_Scen9_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen9_Pgh(2)
>= 0.0

MASTER_c_u_Scen9_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen9_Pgh(2)
<= 0.0

MASTER_c_l_Scen9_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen9_Pgh(1)
>= 0.0

MASTER_c_u_Scen9_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen9_Pgh(1)
<= 0.0

MASTER_c_l_Scen1_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen1_Pgt(2)
>= 0.0

MASTER_c_u_Scen1_Pgt_2_:
+1.000000 MASTER_Node2_1_Pgt(2)
-1.000000 Scen1_Pgt(2)
<= 0.0

MASTER_c_l_Scen9_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen9_PDns(2)
>= 0.0

MASTER_c_u_Scen9_PDns_2_:
+1.000000 MASTER_Node2_3_PDns(2)
-1.000000 Scen9_PDns(2)
<= 0.0

MASTER_c_l_Scen9_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen9_PDns(1)
>= 0.0

MASTER_c_u_Scen9_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen9_PDns(1)
<= 0.0

MASTER_c_l_Scen1_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen1_Pgt(1)
>= 0.0

MASTER_c_u_Scen1_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen1_Pgt(1)
<= 0.0

MASTER_c_l_Scen8_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen8_StageCost(2)
>= 0.0

MASTER_c_u_Scen8_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen8_StageCost(2)
<= 0.0

MASTER_c_l_Scen1_Node3_1_1_StageCost_3_:
+1.000000 MASTER_Node3_1_1_StageCost(3)
-1.000000 Scen1_StageCost(3)
>= 0.0

MASTER_c_u_Scen1_Node3_1_1_StageCost_3_:
+1.000000 MASTER_Node3_1_1_StageCost(3)
-1.000000 Scen1_StageCost(3)
<= 0.0

MASTER_c_l_Scen2_Node3_1_2_StageCost_3_:
+1.000000 MASTER_Node3_1_2_StageCost(3)
-1.000000 Scen2_StageCost(3)
>= 0.0

MASTER_c_u_Scen2_Node3_1_2_StageCost_3_:
+1.000000 MASTER_Node3_1_2_StageCost(3)
-1.000000 Scen2_StageCost(3)
<= 0.0

MASTER_c_l_Scen6_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen6_Pgh(1)
>= 0.0

MASTER_c_u_Scen6_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen6_Pgh(1)
<= 0.0

MASTER_c_l_Scen5_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen5_StageCost(2)
>= 0.0

MASTER_c_u_Scen5_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen5_StageCost(2)
<= 0.0

MASTER_c_l_Scen7_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen7_StageCost(1)
>= 0.0

MASTER_c_u_Scen7_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen7_StageCost(1)
<= 0.0

MASTER_c_l_Scen4_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen4_Pgh(2)
>= 0.0

MASTER_c_u_Scen4_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen4_Pgh(2)
<= 0.0

MASTER_c_l_Scen4_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen4_Pgh(1)
>= 0.0

MASTER_c_u_Scen4_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen4_Pgh(1)
<= 0.0

MASTER_c_l_Scen1_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen1_Pgh(2)
>= 0.0

MASTER_c_u_Scen1_Pgh_2_:
+1.000000 MASTER_Node2_1_Pgh(2)
-1.000000 Scen1_Pgh(2)
<= 0.0

MASTER_c_l_Scen7_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen7_Pgh(1)
>= 0.0

MASTER_c_u_Scen7_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen7_Pgh(1)
<= 0.0

MASTER_c_l_Scen7_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen7_Pgh(2)
>= 0.0

MASTER_c_u_Scen7_Pgh_2_:
+1.000000 MASTER_Node2_3_Pgh(2)
-1.000000 Scen7_Pgh(2)
<= 0.0

MASTER_c_l_Scen1_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen1_Pgh(1)
>= 0.0

MASTER_c_u_Scen1_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen1_Pgh(1)
<= 0.0

MASTER_c_l_COST_Node2_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_3
-0.333000 MASTER_EXPECTED_COST_Node3_3_1
-0.333000 MASTER_EXPECTED_COST_Node3_3_2
-0.334000 MASTER_EXPECTED_COST_Node3_3_3
-1.000000 MASTER_Node2_3_StageCost(2)
>= 0.0

MASTER_c_u_COST_Node2_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_3
-0.333000 MASTER_EXPECTED_COST_Node3_3_1
-0.333000 MASTER_EXPECTED_COST_Node3_3_2
-0.334000 MASTER_EXPECTED_COST_Node3_3_3
-1.000000 MASTER_Node2_3_StageCost(2)
<= 0.0

MASTER_c_l_Scen7_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen7_Pgt(1)
>= 0.0

MASTER_c_u_Scen7_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen7_Pgt(1)
<= 0.0

MASTER_c_l_Scen7_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen7_Pgt(2)
>= 0.0

MASTER_c_u_Scen7_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen7_Pgt(2)
<= 0.0

MASTER_c_l_Scen4_Node3_2_1_StageCost_3_:
+1.000000 MASTER_Node3_2_1_StageCost(3)
-1.000000 Scen4_StageCost(3)
>= 0.0

MASTER_c_u_Scen4_Node3_2_1_StageCost_3_:
+1.000000 MASTER_Node3_2_1_StageCost(3)
-1.000000 Scen4_StageCost(3)
<= 0.0

MASTER_c_l_Scen5_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen5_Pgh(2)
>= 0.0

MASTER_c_u_Scen5_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen5_Pgh(2)
<= 0.0

MASTER_c_l_COST_Node3_1_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_1
-1.000000 MASTER_Node3_1_1_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_1_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_1_1
-1.000000 MASTER_Node3_1_1_StageCost(3)
<= 0.0

MASTER_c_l_Scen5_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen5_Pgh(1)
>= 0.0

MASTER_c_u_Scen5_Pgh_1_:
+1.000000 MASTER_RootNode_Pgh(1)
-1.000000 Scen5_Pgh(1)
<= 0.0

MASTER_c_l_Scen9_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen9_Vol(1)
>= 0.0

MASTER_c_u_Scen9_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen9_Vol(1)
<= 0.0

MASTER_c_l_Scen9_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen9_Vol(2)
>= 0.0

MASTER_c_u_Scen9_Vol_2_:
+1.000000 MASTER_Node2_3_Vol(2)
-1.000000 Scen9_Vol(2)
<= 0.0

MASTER_c_l_Scen4_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen4_StageCost(2)
>= 0.0

MASTER_c_u_Scen4_Node2_2_StageCost_2_:
+1.000000 MASTER_Node2_2_StageCost(2)
-1.000000 Scen4_StageCost(2)
<= 0.0

MASTER_c_l_Scen9_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen9_StageCost(1)
>= 0.0

MASTER_c_u_Scen9_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen9_StageCost(1)
<= 0.0

MASTER_c_l_Scen6_Node3_2_3_StageCost_3_:
+1.000000 MASTER_Node3_2_3_StageCost(3)
-1.000000 Scen6_StageCost(3)
>= 0.0

MASTER_c_u_Scen6_Node3_2_3_StageCost_3_:
+1.000000 MASTER_Node3_2_3_StageCost(3)
-1.000000 Scen6_StageCost(3)
<= 0.0

MASTER_c_l_Scen7_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen7_StageCost(2)
>= 0.0

MASTER_c_u_Scen7_Node2_3_StageCost_2_:
+1.000000 MASTER_Node2_3_StageCost(2)
-1.000000 Scen7_StageCost(2)
<= 0.0

MASTER_c_l_Scen8_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen8_StageCost(1)
>= 0.0

MASTER_c_u_Scen8_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen8_StageCost(1)
<= 0.0

MASTER_c_l_Scen5_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen5_Vol(1)
>= 0.0

MASTER_c_u_Scen5_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen5_Vol(1)
<= 0.0

MASTER_c_l_Scen5_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen5_Vol(2)
>= 0.0

MASTER_c_u_Scen5_Vol_2_:
+1.000000 MASTER_Node2_2_Vol(2)
-1.000000 Scen5_Vol(2)
<= 0.0

MASTER_c_l_Scen3_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen3_StageCost(2)
>= 0.0

MASTER_c_u_Scen3_Node2_1_StageCost_2_:
+1.000000 MASTER_Node2_1_StageCost(2)
-1.000000 Scen3_StageCost(2)
<= 0.0

MASTER_c_l_Scen6_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen6_Pgt(1)
>= 0.0

MASTER_c_u_Scen6_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen6_Pgt(1)
<= 0.0

MASTER_c_l_COST_Node3_3_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_1
-1.000000 MASTER_Node3_3_1_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_3_1_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_1
-1.000000 MASTER_Node3_3_1_StageCost(3)
<= 0.0

MASTER_c_l_Scen3_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen3_PDns(1)
>= 0.0

MASTER_c_u_Scen3_PDns_1_:
+1.000000 MASTER_RootNode_PDns(1)
-1.000000 Scen3_PDns(1)
<= 0.0

MASTER_c_l_COST_Node2_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_2
-0.333000 MASTER_EXPECTED_COST_Node3_2_1
-0.333000 MASTER_EXPECTED_COST_Node3_2_2
-0.334000 MASTER_EXPECTED_COST_Node3_2_3
-1.000000 MASTER_Node2_2_StageCost(2)
>= 0.0

MASTER_c_u_COST_Node2_2_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node2_2
-0.333000 MASTER_EXPECTED_COST_Node3_2_1
-0.333000 MASTER_EXPECTED_COST_Node3_2_2
-0.334000 MASTER_EXPECTED_COST_Node3_2_3
-1.000000 MASTER_Node2_2_StageCost(2)
<= 0.0

MASTER_c_l_Scen3_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen3_PDns(2)
>= 0.0

MASTER_c_u_Scen3_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen3_PDns(2)
<= 0.0

MASTER_c_l_Scen2_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen2_PDns(2)
>= 0.0

MASTER_c_u_Scen2_PDns_2_:
+1.000000 MASTER_Node2_1_PDns(2)
-1.000000 Scen2_PDns(2)
<= 0.0

MASTER_c_l_Scen5_Node3_2_2_StageCost_3_:
+1.000000 MASTER_Node3_2_2_StageCost(3)
-1.000000 Scen5_StageCost(3)
>= 0.0

MASTER_c_u_Scen5_Node3_2_2_StageCost_3_:
+1.000000 MASTER_Node3_2_2_StageCost(3)
-1.000000 Scen5_StageCost(3)
<= 0.0

MASTER_c_l_COST_Node3_3_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_3
-1.000000 MASTER_Node3_3_3_StageCost(3)
>= 0.0

MASTER_c_u_COST_Node3_3_3_StageCost_3_:
+1.000000 MASTER_EXPECTED_COST_Node3_3_3
-1.000000 MASTER_Node3_3_3_StageCost(3)
<= 0.0

MASTER_c_l_Scen6_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen6_Pgh(2)
>= 0.0

MASTER_c_u_Scen6_Pgh_2_:
+1.000000 MASTER_Node2_2_Pgh(2)
-1.000000 Scen6_Pgh(2)
<= 0.0

MASTER_c_l_Scen7_Node3_3_1_StageCost_3_:
+1.000000 MASTER_Node3_3_1_StageCost(3)
-1.000000 Scen7_StageCost(3)
>= 0.0

MASTER_c_u_Scen7_Node3_3_1_StageCost_3_:
+1.000000 MASTER_Node3_3_1_StageCost(3)
-1.000000 Scen7_StageCost(3)
<= 0.0

MASTER_c_l_Scen8_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen8_Pgt(2)
>= 0.0

MASTER_c_u_Scen8_Pgt_2_:
+1.000000 MASTER_Node2_3_Pgt(2)
-1.000000 Scen8_Pgt(2)
<= 0.0

MASTER_c_l_Scen8_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen8_Pgt(1)
>= 0.0

MASTER_c_u_Scen8_Pgt_1_:
+1.000000 MASTER_RootNode_Pgt(1)
-1.000000 Scen8_Pgt(1)
<= 0.0

MASTER_c_l_Scen4_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen4_StageCost(1)
>= 0.0

MASTER_c_u_Scen4_RootNode_StageCost_1_:
+1.000000 MASTER_RootNode_StageCost(1)
-1.000000 Scen4_StageCost(1)
<= 0.0

MASTER_c_l_Scen9_Node3_3_3_StageCost_3_:
+1.000000 MASTER_Node3_3_3_StageCost(3)
-1.000000 Scen9_StageCost(3)
>= 0.0

MASTER_c_u_Scen9_Node3_3_3_StageCost_3_:
+1.000000 MASTER_Node3_3_3_StageCost(3)
-1.000000 Scen9_StageCost(3)
<= 0.0

MASTER_c_l_COST_RootNode_StageCost_3_:
-0.333000 MASTER_EXPECTED_COST_Node2_1
-0.333000 MASTER_EXPECTED_COST_Node2_2
-0.334000 MASTER_EXPECTED_COST_Node2_3
+1.000000 MASTER_EXPECTED_COST_RootNode
-1.000000 MASTER_RootNode_StageCost(1)
>= 0.0

MASTER_c_u_COST_RootNode_StageCost_3_:
-0.333000 MASTER_EXPECTED_COST_Node2_1
-0.333000 MASTER_EXPECTED_COST_Node2_2
-0.334000 MASTER_EXPECTED_COST_Node2_3
+1.000000 MASTER_EXPECTED_COST_RootNode
-1.000000 MASTER_RootNode_StageCost(1)
<= 0.0

MASTER_c_l_Scen2_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen2_Vol(2)
>= 0.0

MASTER_c_u_Scen2_Vol_2_:
+1.000000 MASTER_Node2_1_Vol(2)
-1.000000 Scen2_Vol(2)
<= 0.0

MASTER_c_l_Scen2_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen2_Vol(1)
>= 0.0

MASTER_c_u_Scen2_Vol_1_:
+1.000000 MASTER_RootNode_Vol(1)
-1.000000 Scen2_Vol(1)
<= 0.0

MASTER_c_e_ONE_VAR_CONSTANT: 
MASTER_ONE_VAR_CONSTANT = 1.0

\ End constraint block for master 
\ Begin constraint block for scenario Scen8
Scen8_c_u_conserv(1)_:
+0.604800 Scen8_Pgh(1)
+1.000000 Scen8_Vol(1)
<= 90.72

Scen8_c_u_conserv(2)_:
+0.604800 Scen8_Pgh(2)
-1.000000 Scen8_Vol(1)
+1.000000 Scen8_Vol(2)
<= 54.432

Scen8_c_u_conserv(3)_:
+1.209600 Scen8_Pgh(3)
-1.000000 Scen8_Vol(2)
+1.000000 Scen8_Vol(3)
<= 60.48

Scen8_c_e_StageCostConstraint(1)_:
-10.000000 Scen8_PDns(1)
+0.000000 Scen8_Pgh(1)
-1.000000 Scen8_Pgt(1)
+1.000000 Scen8_StageCost(1)
= 0.0

Scen8_c_e_StageCostConstraint(2)_:
-10.000000 Scen8_PDns(2)
+0.000000 Scen8_Pgh(2)
-1.000000 Scen8_Pgt(2)
+1.000000 Scen8_StageCost(2)
= 0.0

Scen8_c_e_StageCostConstraint(3)_:
-10.000000 Scen8_PDns(3)
+0.000000 Scen8_Pgh(3)
-1.000000 Scen8_Pgt(3)
+1.000000 Scen8_StageCost(3)
-1.000000 Scen8_sl
= 0.0

Scen8_c_u_fcfe_:
-4166.670000 Scen8_Vol(3)
-1.000000 Scen8_sl
<= -252000.2016

Scen8_c_e_demand(1)_:
+1.000000 Scen8_PDns(1)
+1.000000 Scen8_Pgh(1)
+1.000000 Scen8_Pgt(1)
= 90.0

Scen8_c_e_demand(2)_:
+1.000000 Scen8_PDns(2)
+1.000000 Scen8_Pgh(2)
+1.000000 Scen8_Pgt(2)
= 160.0

Scen8_c_e_demand(3)_:
+1.000000 Scen8_PDns(3)
+1.000000 Scen8_Pgh(3)
+1.000000 Scen8_Pgt(3)
= 110.0

Scen8_c_e_ONE_VAR_CONSTANT: 
Scen8_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen8

\ Begin constraint block for scenario Scen9
Scen9_c_u_conserv(1)_:
+0.604800 Scen9_Pgh(1)
+1.000000 Scen9_Vol(1)
<= 90.72

Scen9_c_u_conserv(2)_:
+0.604800 Scen9_Pgh(2)
-1.000000 Scen9_Vol(1)
+1.000000 Scen9_Vol(2)
<= 54.432

Scen9_c_u_conserv(3)_:
+1.209600 Scen9_Pgh(3)
-1.000000 Scen9_Vol(2)
+1.000000 Scen9_Vol(3)
<= 72.576

Scen9_c_e_StageCostConstraint(1)_:
-10.000000 Scen9_PDns(1)
+0.000000 Scen9_Pgh(1)
-1.000000 Scen9_Pgt(1)
+1.000000 Scen9_StageCost(1)
= 0.0

Scen9_c_e_StageCostConstraint(2)_:
-10.000000 Scen9_PDns(2)
+0.000000 Scen9_Pgh(2)
-1.000000 Scen9_Pgt(2)
+1.000000 Scen9_StageCost(2)
= 0.0

Scen9_c_e_StageCostConstraint(3)_:
-10.000000 Scen9_PDns(3)
+0.000000 Scen9_Pgh(3)
-1.000000 Scen9_Pgt(3)
+1.000000 Scen9_StageCost(3)
-1.000000 Scen9_sl
= 0.0

Scen9_c_u_fcfe_:
-4166.670000 Scen9_Vol(3)
-1.000000 Scen9_sl
<= -252000.2016

Scen9_c_e_demand(1)_:
+1.000000 Scen9_PDns(1)
+1.000000 Scen9_Pgh(1)
+1.000000 Scen9_Pgt(1)
= 90.0

Scen9_c_e_demand(2)_:
+1.000000 Scen9_PDns(2)
+1.000000 Scen9_Pgh(2)
+1.000000 Scen9_Pgt(2)
= 160.0

Scen9_c_e_demand(3)_:
+1.000000 Scen9_PDns(3)
+1.000000 Scen9_Pgh(3)
+1.000000 Scen9_Pgt(3)
= 110.0

Scen9_c_e_ONE_VAR_CONSTANT: 
Scen9_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen9

\ Begin constraint block for scenario Scen1
Scen1_c_u_conserv(1)_:
+0.604800 Scen1_Pgh(1)
+1.000000 Scen1_Vol(1)
<= 90.72

Scen1_c_u_conserv(2)_:
+0.604800 Scen1_Pgh(2)
-1.000000 Scen1_Vol(1)
+1.000000 Scen1_Vol(2)
<= 6.048

Scen1_c_u_conserv(3)_:
+1.209600 Scen1_Pgh(3)
-1.000000 Scen1_Vol(2)
+1.000000 Scen1_Vol(3)
<= 48.384

Scen1_c_e_StageCostConstraint(1)_:
-10.000000 Scen1_PDns(1)
+0.000000 Scen1_Pgh(1)
-1.000000 Scen1_Pgt(1)
+1.000000 Scen1_StageCost(1)
= 0.0

Scen1_c_e_StageCostConstraint(2)_:
-10.000000 Scen1_PDns(2)
+0.000000 Scen1_Pgh(2)
-1.000000 Scen1_Pgt(2)
+1.000000 Scen1_StageCost(2)
= 0.0

Scen1_c_e_StageCostConstraint(3)_:
-10.000000 Scen1_PDns(3)
+0.000000 Scen1_Pgh(3)
-1.000000 Scen1_Pgt(3)
+1.000000 Scen1_StageCost(3)
-1.000000 Scen1_sl
= 0.0

Scen1_c_u_fcfe_:
-4166.670000 Scen1_Vol(3)
-1.000000 Scen1_sl
<= -252000.2016

Scen1_c_e_demand(1)_:
+1.000000 Scen1_PDns(1)
+1.000000 Scen1_Pgh(1)
+1.000000 Scen1_Pgt(1)
= 90.0

Scen1_c_e_demand(2)_:
+1.000000 Scen1_PDns(2)
+1.000000 Scen1_Pgh(2)
+1.000000 Scen1_Pgt(2)
= 160.0

Scen1_c_e_demand(3)_:
+1.000000 Scen1_PDns(3)
+1.000000 Scen1_Pgh(3)
+1.000000 Scen1_Pgt(3)
= 110.0

Scen1_c_e_ONE_VAR_CONSTANT: 
Scen1_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen1

\ Begin constraint block for scenario Scen2
Scen2_c_u_conserv(1)_:
+0.604800 Scen2_Pgh(1)
+1.000000 Scen2_Vol(1)
<= 90.72

Scen2_c_u_conserv(2)_:
+0.604800 Scen2_Pgh(2)
-1.000000 Scen2_Vol(1)
+1.000000 Scen2_Vol(2)
<= 6.048

Scen2_c_u_conserv(3)_:
+1.209600 Scen2_Pgh(3)
-1.000000 Scen2_Vol(2)
+1.000000 Scen2_Vol(3)
<= 60.48

Scen2_c_e_StageCostConstraint(1)_:
-10.000000 Scen2_PDns(1)
+0.000000 Scen2_Pgh(1)
-1.000000 Scen2_Pgt(1)
+1.000000 Scen2_StageCost(1)
= 0.0

Scen2_c_e_StageCostConstraint(2)_:
-10.000000 Scen2_PDns(2)
+0.000000 Scen2_Pgh(2)
-1.000000 Scen2_Pgt(2)
+1.000000 Scen2_StageCost(2)
= 0.0

Scen2_c_e_StageCostConstraint(3)_:
-10.000000 Scen2_PDns(3)
+0.000000 Scen2_Pgh(3)
-1.000000 Scen2_Pgt(3)
+1.000000 Scen2_StageCost(3)
-1.000000 Scen2_sl
= 0.0

Scen2_c_u_fcfe_:
-4166.670000 Scen2_Vol(3)
-1.000000 Scen2_sl
<= -252000.2016

Scen2_c_e_demand(1)_:
+1.000000 Scen2_PDns(1)
+1.000000 Scen2_Pgh(1)
+1.000000 Scen2_Pgt(1)
= 90.0

Scen2_c_e_demand(2)_:
+1.000000 Scen2_PDns(2)
+1.000000 Scen2_Pgh(2)
+1.000000 Scen2_Pgt(2)
= 160.0

Scen2_c_e_demand(3)_:
+1.000000 Scen2_PDns(3)
+1.000000 Scen2_Pgh(3)
+1.000000 Scen2_Pgt(3)
= 110.0

Scen2_c_e_ONE_VAR_CONSTANT: 
Scen2_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen2

\ Begin constraint block for scenario Scen3
Scen3_c_u_conserv(1)_:
+0.604800 Scen3_Pgh(1)
+1.000000 Scen3_Vol(1)
<= 90.72

Scen3_c_u_conserv(2)_:
+0.604800 Scen3_Pgh(2)
-1.000000 Scen3_Vol(1)
+1.000000 Scen3_Vol(2)
<= 6.048

Scen3_c_u_conserv(3)_:
+1.209600 Scen3_Pgh(3)
-1.000000 Scen3_Vol(2)
+1.000000 Scen3_Vol(3)
<= 72.576

Scen3_c_e_StageCostConstraint(1)_:
-10.000000 Scen3_PDns(1)
+0.000000 Scen3_Pgh(1)
-1.000000 Scen3_Pgt(1)
+1.000000 Scen3_StageCost(1)
= 0.0

Scen3_c_e_StageCostConstraint(2)_:
-10.000000 Scen3_PDns(2)
+0.000000 Scen3_Pgh(2)
-1.000000 Scen3_Pgt(2)
+1.000000 Scen3_StageCost(2)
= 0.0

Scen3_c_e_StageCostConstraint(3)_:
-10.000000 Scen3_PDns(3)
+0.000000 Scen3_Pgh(3)
-1.000000 Scen3_Pgt(3)
+1.000000 Scen3_StageCost(3)
-1.000000 Scen3_sl
= 0.0

Scen3_c_u_fcfe_:
-4166.670000 Scen3_Vol(3)
-1.000000 Scen3_sl
<= -252000.2016

Scen3_c_e_demand(1)_:
+1.000000 Scen3_PDns(1)
+1.000000 Scen3_Pgh(1)
+1.000000 Scen3_Pgt(1)
= 90.0

Scen3_c_e_demand(2)_:
+1.000000 Scen3_PDns(2)
+1.000000 Scen3_Pgh(2)
+1.000000 Scen3_Pgt(2)
= 160.0

Scen3_c_e_demand(3)_:
+1.000000 Scen3_PDns(3)
+1.000000 Scen3_Pgh(3)
+1.000000 Scen3_Pgt(3)
= 110.0

Scen3_c_e_ONE_VAR_CONSTANT: 
Scen3_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen3

\ Begin constraint block for scenario Scen4
Scen4_c_u_conserv(1)_:
+0.604800 Scen4_Pgh(1)
+1.000000 Scen4_Vol(1)
<= 90.72

Scen4_c_u_conserv(2)_:
+0.604800 Scen4_Pgh(2)
-1.000000 Scen4_Vol(1)
+1.000000 Scen4_Vol(2)
<= 30.24

Scen4_c_u_conserv(3)_:
+1.209600 Scen4_Pgh(3)
-1.000000 Scen4_Vol(2)
+1.000000 Scen4_Vol(3)
<= 48.384

Scen4_c_e_StageCostConstraint(1)_:
-10.000000 Scen4_PDns(1)
+0.000000 Scen4_Pgh(1)
-1.000000 Scen4_Pgt(1)
+1.000000 Scen4_StageCost(1)
= 0.0

Scen4_c_e_StageCostConstraint(2)_:
-10.000000 Scen4_PDns(2)
+0.000000 Scen4_Pgh(2)
-1.000000 Scen4_Pgt(2)
+1.000000 Scen4_StageCost(2)
= 0.0

Scen4_c_e_StageCostConstraint(3)_:
-10.000000 Scen4_PDns(3)
+0.000000 Scen4_Pgh(3)
-1.000000 Scen4_Pgt(3)
+1.000000 Scen4_StageCost(3)
-1.000000 Scen4_sl
= 0.0

Scen4_c_u_fcfe_:
-4166.670000 Scen4_Vol(3)
-1.000000 Scen4_sl
<= -252000.2016

Scen4_c_e_demand(1)_:
+1.000000 Scen4_PDns(1)
+1.000000 Scen4_Pgh(1)
+1.000000 Scen4_Pgt(1)
= 90.0

Scen4_c_e_demand(2)_:
+1.000000 Scen4_PDns(2)
+1.000000 Scen4_Pgh(2)
+1.000000 Scen4_Pgt(2)
= 160.0

Scen4_c_e_demand(3)_:
+1.000000 Scen4_PDns(3)
+1.000000 Scen4_Pgh(3)
+1.000000 Scen4_Pgt(3)
= 110.0

Scen4_c_e_ONE_VAR_CONSTANT: 
Scen4_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen4

\ Begin constraint block for scenario Scen5
Scen5_c_u_conserv(1)_:
+0.604800 Scen5_Pgh(1)
+1.000000 Scen5_Vol(1)
<= 90.72

Scen5_c_u_conserv(2)_:
+0.604800 Scen5_Pgh(2)
-1.000000 Scen5_Vol(1)
+1.000000 Scen5_Vol(2)
<= 30.24

Scen5_c_u_conserv(3)_:
+1.209600 Scen5_Pgh(3)
-1.000000 Scen5_Vol(2)
+1.000000 Scen5_Vol(3)
<= 60.48

Scen5_c_e_StageCostConstraint(1)_:
-10.000000 Scen5_PDns(1)
+0.000000 Scen5_Pgh(1)
-1.000000 Scen5_Pgt(1)
+1.000000 Scen5_StageCost(1)
= 0.0

Scen5_c_e_StageCostConstraint(2)_:
-10.000000 Scen5_PDns(2)
+0.000000 Scen5_Pgh(2)
-1.000000 Scen5_Pgt(2)
+1.000000 Scen5_StageCost(2)
= 0.0

Scen5_c_e_StageCostConstraint(3)_:
-10.000000 Scen5_PDns(3)
+0.000000 Scen5_Pgh(3)
-1.000000 Scen5_Pgt(3)
+1.000000 Scen5_StageCost(3)
-1.000000 Scen5_sl
= 0.0

Scen5_c_u_fcfe_:
-4166.670000 Scen5_Vol(3)
-1.000000 Scen5_sl
<= -252000.2016

Scen5_c_e_demand(1)_:
+1.000000 Scen5_PDns(1)
+1.000000 Scen5_Pgh(1)
+1.000000 Scen5_Pgt(1)
= 90.0

Scen5_c_e_demand(2)_:
+1.000000 Scen5_PDns(2)
+1.000000 Scen5_Pgh(2)
+1.000000 Scen5_Pgt(2)
= 160.0

Scen5_c_e_demand(3)_:
+1.000000 Scen5_PDns(3)
+1.000000 Scen5_Pgh(3)
+1.000000 Scen5_Pgt(3)
= 110.0

Scen5_c_e_ONE_VAR_CONSTANT: 
Scen5_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen5

\ Begin constraint block for scenario Scen6
Scen6_c_u_conserv(1)_:
+0.604800 Scen6_Pgh(1)
+1.000000 Scen6_Vol(1)
<= 90.72

Scen6_c_u_conserv(2)_:
+0.604800 Scen6_Pgh(2)
-1.000000 Scen6_Vol(1)
+1.000000 Scen6_Vol(2)
<= 30.24

Scen6_c_u_conserv(3)_:
+1.209600 Scen6_Pgh(3)
-1.000000 Scen6_Vol(2)
+1.000000 Scen6_Vol(3)
<= 72.576

Scen6_c_e_StageCostConstraint(1)_:
-10.000000 Scen6_PDns(1)
+0.000000 Scen6_Pgh(1)
-1.000000 Scen6_Pgt(1)
+1.000000 Scen6_StageCost(1)
= 0.0

Scen6_c_e_StageCostConstraint(2)_:
-10.000000 Scen6_PDns(2)
+0.000000 Scen6_Pgh(2)
-1.000000 Scen6_Pgt(2)
+1.000000 Scen6_StageCost(2)
= 0.0

Scen6_c_e_StageCostConstraint(3)_:
-10.000000 Scen6_PDns(3)
+0.000000 Scen6_Pgh(3)
-1.000000 Scen6_Pgt(3)
+1.000000 Scen6_StageCost(3)
-1.000000 Scen6_sl
= 0.0

Scen6_c_u_fcfe_:
-4166.670000 Scen6_Vol(3)
-1.000000 Scen6_sl
<= -252000.2016

Scen6_c_e_demand(1)_:
+1.000000 Scen6_PDns(1)
+1.000000 Scen6_Pgh(1)
+1.000000 Scen6_Pgt(1)
= 90.0

Scen6_c_e_demand(2)_:
+1.000000 Scen6_PDns(2)
+1.000000 Scen6_Pgh(2)
+1.000000 Scen6_Pgt(2)
= 160.0

Scen6_c_e_demand(3)_:
+1.000000 Scen6_PDns(3)
+1.000000 Scen6_Pgh(3)
+1.000000 Scen6_Pgt(3)
= 110.0

Scen6_c_e_ONE_VAR_CONSTANT: 
Scen6_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen6

\ Begin constraint block for scenario Scen7
Scen7_c_u_conserv(1)_:
+0.604800 Scen7_Pgh(1)
+1.000000 Scen7_Vol(1)
<= 90.72

Scen7_c_u_conserv(2)_:
+0.604800 Scen7_Pgh(2)
-1.000000 Scen7_Vol(1)
+1.000000 Scen7_Vol(2)
<= 54.432

Scen7_c_u_conserv(3)_:
+1.209600 Scen7_Pgh(3)
-1.000000 Scen7_Vol(2)
+1.000000 Scen7_Vol(3)
<= 48.384

Scen7_c_e_StageCostConstraint(1)_:
-10.000000 Scen7_PDns(1)
+0.000000 Scen7_Pgh(1)
-1.000000 Scen7_Pgt(1)
+1.000000 Scen7_StageCost(1)
= 0.0

Scen7_c_e_StageCostConstraint(2)_:
-10.000000 Scen7_PDns(2)
+0.000000 Scen7_Pgh(2)
-1.000000 Scen7_Pgt(2)
+1.000000 Scen7_StageCost(2)
= 0.0

Scen7_c_e_StageCostConstraint(3)_:
-10.000000 Scen7_PDns(3)
+0.000000 Scen7_Pgh(3)
-1.000000 Scen7_Pgt(3)
+1.000000 Scen7_StageCost(3)
-1.000000 Scen7_sl
= 0.0

Scen7_c_u_fcfe_:
-4166.670000 Scen7_Vol(3)
-1.000000 Scen7_sl
<= -252000.2016

Scen7_c_e_demand(1)_:
+1.000000 Scen7_PDns(1)
+1.000000 Scen7_Pgh(1)
+1.000000 Scen7_Pgt(1)
= 90.0

Scen7_c_e_demand(2)_:
+1.000000 Scen7_PDns(2)
+1.000000 Scen7_Pgh(2)
+1.000000 Scen7_Pgt(2)
= 160.0

Scen7_c_e_demand(3)_:
+1.000000 Scen7_PDns(3)
+1.000000 Scen7_Pgh(3)
+1.000000 Scen7_Pgt(3)
= 110.0

Scen7_c_e_ONE_VAR_CONSTANT: 
Scen7_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario Scen7

bounds

\ Begin variable bounds block for master
     -inf <=  MASTER_EXPECTED_COST_Node2_1  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node2_2  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node2_3  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_1_1  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_1_2  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_1_3  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_2_1  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_2_2  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_2_3  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_3_1  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_3_2  <= +inf
     -inf <=  MASTER_EXPECTED_COST_Node3_3_3  <= +inf
     -inf <=  MASTER_EXPECTED_COST_RootNode  <= +inf
     -inf <=  MASTER_Node2_1_PDns(2)  <= +inf
     -inf <=  MASTER_Node2_1_Pgh(2)  <= +inf
     -inf <=  MASTER_Node2_1_Pgt(2)  <= +inf
     -inf <=  MASTER_Node2_1_StageCost(2)  <= +inf
     -inf <=  MASTER_Node2_1_Vol(2)  <= +inf
     -inf <=  MASTER_Node2_2_PDns(2)  <= +inf
     -inf <=  MASTER_Node2_2_Pgh(2)  <= +inf
     -inf <=  MASTER_Node2_2_Pgt(2)  <= +inf
     -inf <=  MASTER_Node2_2_StageCost(2)  <= +inf
     -inf <=  MASTER_Node2_2_Vol(2)  <= +inf
     -inf <=  MASTER_Node2_3_PDns(2)  <= +inf
     -inf <=  MASTER_Node2_3_Pgh(2)  <= +inf
     -inf <=  MASTER_Node2_3_Pgt(2)  <= +inf
     -inf <=  MASTER_Node2_3_StageCost(2)  <= +inf
     -inf <=  MASTER_Node2_3_Vol(2)  <= +inf
     -inf <=  MASTER_Node3_1_1_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_1_2_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_1_3_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_2_1_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_2_2_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_2_3_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_3_1_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_3_2_StageCost(3)  <= +inf
     -inf <=  MASTER_Node3_3_3_StageCost(3)  <= +inf
     -inf <=  MASTER_RootNode_PDns(1)  <= +inf
     -inf <=  MASTER_RootNode_Pgh(1)  <= +inf
     -inf <=  MASTER_RootNode_Pgt(1)  <= +inf
     -inf <=  MASTER_RootNode_StageCost(1)  <= +inf
     -inf <=  MASTER_RootNode_Vol(1)  <= +inf
\ End variable bounds block for master

\ Begin variable bounds block for scenario Scen8
    0 <=  Scen8_PDns(1)  <= 90
    0 <=  Scen8_PDns(2)  <= 160
    0 <=  Scen8_PDns(3)  <= 110
    0 <=  Scen8_Pgh(1)  <= 100
    0 <=  Scen8_Pgh(2)  <= 100
    0 <=  Scen8_Pgh(3)  <= 100
    0 <=  Scen8_Pgt(1)  <= 100
    0 <=  Scen8_Pgt(2)  <= 100
    0 <=  Scen8_Pgt(3)  <= 100
     -inf <=  Scen8_StageCost(1)  <= +inf
     -inf <=  Scen8_StageCost(2)  <= +inf
     -inf <=  Scen8_StageCost(3)  <= +inf
    0 <=  Scen8_Vol(1)  <= 100
    0 <=  Scen8_Vol(2)  <= 100
    0 <=  Scen8_Vol(3)  <= 100
    0 <=  Scen8_sl  <= +inf
\ End variable bounds block for scenario Scen8

\ Begin variable bounds block for scenario Scen9
    0 <=  Scen9_PDns(1)  <= 90
    0 <=  Scen9_PDns(2)  <= 160
    0 <=  Scen9_PDns(3)  <= 110
    0 <=  Scen9_Pgh(1)  <= 100
    0 <=  Scen9_Pgh(2)  <= 100
    0 <=  Scen9_Pgh(3)  <= 100
    0 <=  Scen9_Pgt(1)  <= 100
    0 <=  Scen9_Pgt(2)  <= 100
    0 <=  Scen9_Pgt(3)  <= 100
     -inf <=  Scen9_StageCost(1)  <= +inf
     -inf <=  Scen9_StageCost(2)  <= +inf
     -inf <=  Scen9_StageCost(3)  <= +inf
    0 <=  Scen9_Vol(1)  <= 100
    0 <=  Scen9_Vol(2)  <= 100
    0 <=  Scen9_Vol(3)  <= 100
    0 <=  Scen9_sl  <= +inf
\ End variable bounds block for scenario Scen9

\ Begin variable bounds block for scenario Scen1
    0 <=  Scen1_PDns(1)  <= 90
    0 <=  Scen1_PDns(2)  <= 160
    0 <=  Scen1_PDns(3)  <= 110
    0 <=  Scen1_Pgh(1)  <= 100
    0 <=  Scen1_Pgh(2)  <= 100
    0 <=  Scen1_Pgh(3)  <= 100
    0 <=  Scen1_Pgt(1)  <= 100
    0 <=  Scen1_Pgt(2)  <= 100
    0 <=  Scen1_Pgt(3)  <= 100
     -inf <=  Scen1_StageCost(1)  <= +inf
     -inf <=  Scen1_StageCost(2)  <= +inf
     -inf <=  Scen1_StageCost(3)  <= +inf
    0 <=  Scen1_Vol(1)  <= 100
    0 <=  Scen1_Vol(2)  <= 100
    0 <=  Scen1_Vol(3)  <= 100
    0 <=  Scen1_sl  <= +inf
\ End variable bounds block for scenario Scen1

\ Begin variable bounds block for scenario Scen2
    0 <=  Scen2_PDns(1)  <= 90
    0 <=  Scen2_PDns(2)  <= 160
    0 <=  Scen2_PDns(3)  <= 110
    0 <=  Scen2_Pgh(1)  <= 100
    0 <=  Scen2_Pgh(2)  <= 100
    0 <=  Scen2_Pgh(3)  <= 100
    0 <=  Scen2_Pgt(1)  <= 100
    0 <=  Scen2_Pgt(2)  <= 100
    0 <=  Scen2_Pgt(3)  <= 100
     -inf <=  Scen2_StageCost(1)  <= +inf
     -inf <=  Scen2_StageCost(2)  <= +inf
     -inf <=  Scen2_StageCost(3)  <= +inf
    0 <=  Scen2_Vol(1)  <= 100
    0 <=  Scen2_Vol(2)  <= 100
    0 <=  Scen2_Vol(3)  <= 100
    0 <=  Scen2_sl  <= +inf
\ End variable bounds block for scenario Scen2

\ Begin variable bounds block for scenario Scen3
    0 <=  Scen3_PDns(1)  <= 90
    0 <=  Scen3_PDns(2)  <= 160
    0 <=  Scen3_PDns(3)  <= 110
    0 <=  Scen3_Pgh(1)  <= 100
    0 <=  Scen3_Pgh(2)  <= 100
    0 <=  Scen3_Pgh(3)  <= 100
    0 <=  Scen3_Pgt(1)  <= 100
    0 <=  Scen3_Pgt(2)  <= 100
    0 <=  Scen3_Pgt(3)  <= 100
     -inf <=  Scen3_StageCost(1)  <= +inf
     -inf <=  Scen3_StageCost(2)  <= +inf
     -inf <=  Scen3_StageCost(3)  <= +inf
    0 <=  Scen3_Vol(1)  <= 100
    0 <=  Scen3_Vol(2)  <= 100
    0 <=  Scen3_Vol(3)  <= 100
    0 <=  Scen3_sl  <= +inf
\ End variable bounds block for scenario Scen3

\ Begin variable bounds block for scenario Scen4
    0 <=  Scen4_PDns(1)  <= 90
    0 <=  Scen4_PDns(2)  <= 160
    0 <=  Scen4_PDns(3)  <= 110
    0 <=  Scen4_Pgh(1)  <= 100
    0 <=  Scen4_Pgh(2)  <= 100
    0 <=  Scen4_Pgh(3)  <= 100
    0 <=  Scen4_Pgt(1)  <= 100
    0 <=  Scen4_Pgt(2)  <= 100
    0 <=  Scen4_Pgt(3)  <= 100
     -inf <=  Scen4_StageCost(1)  <= +inf
     -inf <=  Scen4_StageCost(2)  <= +inf
     -inf <=  Scen4_StageCost(3)  <= +inf
    0 <=  Scen4_Vol(1)  <= 100
    0 <=  Scen4_Vol(2)  <= 100
    0 <=  Scen4_Vol(3)  <= 100
    0 <=  Scen4_sl  <= +inf
\ End variable bounds block for scenario Scen4

\ Begin variable bounds block for scenario Scen5
    0 <=  Scen5_PDns(1)  <= 90
    0 <=  Scen5_PDns(2)  <= 160
    0 <=  Scen5_PDns(3)  <= 110
    0 <=  Scen5_Pgh(1)  <= 100
    0 <=  Scen5_Pgh(2)  <= 100
    0 <=  Scen5_Pgh(3)  <= 100
    0 <=  Scen5_Pgt(1)  <= 100
    0 <=  Scen5_Pgt(2)  <= 100
    0 <=  Scen5_Pgt(3)  <= 100
     -inf <=  Scen5_StageCost(1)  <= +inf
     -inf <=  Scen5_StageCost(2)  <= +inf
     -inf <=  Scen5_StageCost(3)  <= +inf
    0 <=  Scen5_Vol(1)  <= 100
    0 <=  Scen5_Vol(2)  <= 100
    0 <=  Scen5_Vol(3)  <= 100
    0 <=  Scen5_sl  <= +inf
\ End variable bounds block for scenario Scen5

\ Begin variable bounds block for scenario Scen6
    0 <=  Scen6_PDns(1)  <= 90
    0 <=  Scen6_PDns(2)  <= 160
    0 <=  Scen6_PDns(3)  <= 110
    0 <=  Scen6_Pgh(1)  <= 100
    0 <=  Scen6_Pgh(2)  <= 100
    0 <=  Scen6_Pgh(3)  <= 100
    0 <=  Scen6_Pgt(1)  <= 100
    0 <=  Scen6_Pgt(2)  <= 100
    0 <=  Scen6_Pgt(3)  <= 100
     -inf <=  Scen6_StageCost(1)  <= +inf
     -inf <=  Scen6_StageCost(2)  <= +inf
     -inf <=  Scen6_StageCost(3)  <= +inf
    0 <=  Scen6_Vol(1)  <= 100
    0 <=  Scen6_Vol(2)  <= 100
    0 <=  Scen6_Vol(3)  <= 100
    0 <=  Scen6_sl  <= +inf
\ End variable bounds block for scenario Scen6

\ Begin variable bounds block for scenario Scen7
    0 <=  Scen7_PDns(1)  <= 90
    0 <=  Scen7_PDns(2)  <= 160
    0 <=  Scen7_PDns(3)  <= 110
    0 <=  Scen7_Pgh(1)  <= 100
    0 <=  Scen7_Pgh(2)  <= 100
    0 <=  Scen7_Pgh(3)  <= 100
    0 <=  Scen7_Pgt(1)  <= 100
    0 <=  Scen7_Pgt(2)  <= 100
    0 <=  Scen7_Pgt(3)  <= 100
     -inf <=  Scen7_StageCost(1)  <= +inf
     -inf <=  Scen7_StageCost(2)  <= +inf
     -inf <=  Scen7_StageCost(3)  <= +inf
    0 <=  Scen7_Vol(1)  <= 100
    0 <=  Scen7_Vol(2)  <= 100
    0 <=  Scen7_Vol(3)  <= 100
    0 <=  Scen7_sl  <= +inf
\ End variable bounds block for scenario Scen7

end
