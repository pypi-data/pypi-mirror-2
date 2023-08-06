\ Begin objective block for master
min 
MASTER:
+1.000000 MASTER_CVAR_COST_RootNode

\ End objective block for master

s.t.

\ Begin constraint block for master
MASTER_c_l_AverageScenario_AverageNode_SecondStageCost_None_:
-1.000000 AverageScenario_SecondStageCost
+1.000000 MASTER_AverageNode_SecondStageCost
>= 0.0

MASTER_c_u_AverageScenario_AverageNode_SecondStageCost_None_:
-1.000000 AverageScenario_SecondStageCost
+1.000000 MASTER_AverageNode_SecondStageCost
<= 0.0

MASTER_c_l_AboveAverageScenario_DevotedAcreage_CORN_:
-1.000000 AboveAverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
>= 0.0

MASTER_c_u_AboveAverageScenario_DevotedAcreage_CORN_:
-1.000000 AboveAverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
<= 0.0

MASTER_c_l_AverageScenario_DevotedAcreage_CORN_:
-1.000000 AverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
>= 0.0

MASTER_c_u_AverageScenario_DevotedAcreage_CORN_:
-1.000000 AverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
<= 0.0

MASTER_c_l_AverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
>= 0.0

MASTER_c_u_AverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
<= 0.0

MASTER_c_l_BelowAverageScenario_DevotedAcreage_CORN_:
-1.000000 BelowAverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
>= 0.0

MASTER_c_u_BelowAverageScenario_DevotedAcreage_CORN_:
-1.000000 BelowAverageScenario_DevotedAcreage(CORN)
+1.000000 MASTER_RootNode_DevotedAcreage(CORN)
<= 0.0

MASTER_c_l_AboveAverageScenario_AboveAverageNode_SecondStageCost_None_:
-1.000000 AboveAverageScenario_SecondStageCost
+1.000000 MASTER_AboveAverageNode_SecondStageCost
>= 0.0

MASTER_c_u_AboveAverageScenario_AboveAverageNode_SecondStageCost_None_:
-1.000000 AboveAverageScenario_SecondStageCost
+1.000000 MASTER_AboveAverageNode_SecondStageCost
<= 0.0

MASTER_c_l_AboveAverageScenario_DevotedAcreage_WHEAT_:
-1.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
>= 0.0

MASTER_c_u_AboveAverageScenario_DevotedAcreage_WHEAT_:
-1.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
<= 0.0

MASTER_c_l_AboveAverageScenario_CVAR_ETA_None_:
-1.000000 AboveAverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
>= 0.0

MASTER_c_u_AboveAverageScenario_CVAR_ETA_None_:
-1.000000 AboveAverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
<= 0.0

MASTER_c_l_AboveAverageScenario_RootNode_FirstStageCost_None_:
-1.000000 AboveAverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
>= 0.0

MASTER_c_u_AboveAverageScenario_RootNode_FirstStageCost_None_:
-1.000000 AboveAverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
<= 0.0

MASTER_c_l_BelowAverageScenario_RootNode_FirstStageCost_None_:
-1.000000 BelowAverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
>= 0.0

MASTER_c_u_BelowAverageScenario_RootNode_FirstStageCost_None_:
-1.000000 BelowAverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
<= 0.0

MASTER_c_l_COST_AverageNode_SecondStageCost_None_:
-1.000000 MASTER_AverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_AverageNode
>= 0.0

MASTER_c_u_COST_AverageNode_SecondStageCost_None_:
-1.000000 MASTER_AverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_AverageNode
<= 0.0

MASTER_c_l_AboveAverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
>= 0.0

MASTER_c_u_AboveAverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
<= 0.0

MASTER_c_l_AverageScenario_RootNode_FirstStageCost_None_:
-1.000000 AverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
>= 0.0

MASTER_c_u_AverageScenario_RootNode_FirstStageCost_None_:
-1.000000 AverageScenario_FirstStageCost
+1.000000 MASTER_RootNode_FirstStageCost
<= 0.0

MASTER_c_l_COST_BelowAverageNode_SecondStageCost_None_:
-1.000000 MASTER_BelowAverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_BelowAverageNode
>= 0.0

MASTER_c_u_COST_BelowAverageNode_SecondStageCost_None_:
-1.000000 MASTER_BelowAverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_BelowAverageNode
<= 0.0

MASTER_c_l_AverageScenario_DevotedAcreage_WHEAT_:
-1.000000 AverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
>= 0.0

MASTER_c_u_AverageScenario_DevotedAcreage_WHEAT_:
-1.000000 AverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
<= 0.0

MASTER_c_l_COST_RootNode_FirstStageCost_None_:
-0.333333 MASTER_EXPECTED_COST_AboveAverageNode
-0.333333 MASTER_EXPECTED_COST_AverageNode
-0.333333 MASTER_EXPECTED_COST_BelowAverageNode
+1.000000 MASTER_EXPECTED_COST_RootNode
-1.000000 MASTER_RootNode_FirstStageCost
>= 0.0

MASTER_c_u_COST_RootNode_FirstStageCost_None_:
-0.333333 MASTER_EXPECTED_COST_AboveAverageNode
-0.333333 MASTER_EXPECTED_COST_AverageNode
-0.333333 MASTER_EXPECTED_COST_BelowAverageNode
+1.000000 MASTER_EXPECTED_COST_RootNode
-1.000000 MASTER_RootNode_FirstStageCost
<= 0.0

MASTER_c_l_COST_AboveAverageNode_SecondStageCost_None_:
-1.000000 MASTER_AboveAverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_AboveAverageNode
>= 0.0

MASTER_c_u_COST_AboveAverageNode_SecondStageCost_None_:
-1.000000 MASTER_AboveAverageNode_SecondStageCost
+1.000000 MASTER_EXPECTED_COST_AboveAverageNode
<= 0.0

MASTER_c_l_BelowAverageScenario_CVAR_ETA_None_:
-1.000000 BelowAverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
>= 0.0

MASTER_c_u_BelowAverageScenario_CVAR_ETA_None_:
-1.000000 BelowAverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
<= 0.0

MASTER_c_l_BelowAverageScenario_BelowAverageNode_SecondStageCost_None_:
-1.000000 BelowAverageScenario_SecondStageCost
+1.000000 MASTER_BelowAverageNode_SecondStageCost
>= 0.0

MASTER_c_u_BelowAverageScenario_BelowAverageNode_SecondStageCost_None_:
-1.000000 BelowAverageScenario_SecondStageCost
+1.000000 MASTER_BelowAverageNode_SecondStageCost
<= 0.0

MASTER_c_l_BelowAverageScenario_DevotedAcreage_WHEAT_:
-1.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
>= 0.0

MASTER_c_u_BelowAverageScenario_DevotedAcreage_WHEAT_:
-1.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
+1.000000 MASTER_RootNode_DevotedAcreage(WHEAT)
<= 0.0

MASTER_c_l_COMPUTE_CVAR_COST_:
-3.333333 AboveAverageScenario_CVAR_EXCESS
-3.333333 AverageScenario_CVAR_EXCESS
-3.333333 BelowAverageScenario_CVAR_EXCESS
+1.000000 MASTER_CVAR_COST_RootNode
-1.000000 MASTER_RootNode_CVAR_ETA
>= 0.0

MASTER_c_u_COMPUTE_CVAR_COST_:
-3.333333 AboveAverageScenario_CVAR_EXCESS
-3.333333 AverageScenario_CVAR_EXCESS
-3.333333 BelowAverageScenario_CVAR_EXCESS
+1.000000 MASTER_CVAR_COST_RootNode
-1.000000 MASTER_RootNode_CVAR_ETA
<= 0.0

MASTER_c_l_BelowAverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
>= 0.0

MASTER_c_u_BelowAverageScenario_DevotedAcreage_SUGAR_BEETS_:
-1.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)
<= 0.0

MASTER_c_l_AverageScenario_CVAR_ETA_None_:
-1.000000 AverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
>= 0.0

MASTER_c_u_AverageScenario_CVAR_ETA_None_:
-1.000000 AverageScenario_CVAR_ETA
+1.000000 MASTER_RootNode_CVAR_ETA
<= 0.0

MASTER_c_e_ONE_VAR_CONSTANT: 
MASTER_ONE_VAR_CONSTANT = 1.0

\ End constraint block for master 
\ Begin constraint block for scenario AverageScenario
AverageScenario_c_e_ComputeSecondStageCost_:
-210.000000 AverageScenario_QuantityPurchased(CORN)
-100000.000000 AverageScenario_QuantityPurchased(SUGAR_BEETS)
-238.000000 AverageScenario_QuantityPurchased(WHEAT)
+150.000000 AverageScenario_QuantitySubQuotaSold(CORN)
+36.000000 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+170.000000 AverageScenario_QuantitySubQuotaSold(WHEAT)
+0.000000 AverageScenario_QuantitySuperQuotaSold(CORN)
+10.000000 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
+0.000000 AverageScenario_QuantitySuperQuotaSold(WHEAT)
+1.000000 AverageScenario_SecondStageCost
= 0.0

AverageScenario_c_u_LimitAmountSold(CORN)_:
-3.000000 AverageScenario_DevotedAcreage(CORN)
+1.000000 AverageScenario_QuantitySubQuotaSold(CORN)
+1.000000 AverageScenario_QuantitySuperQuotaSold(CORN)
<= 0.0

AverageScenario_c_u_LimitAmountSold(SUGAR_BEETS)_:
-20.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1.000000 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0.0

AverageScenario_c_u_LimitAmountSold(WHEAT)_:
-2.500000 AverageScenario_DevotedAcreage(WHEAT)
+1.000000 AverageScenario_QuantitySubQuotaSold(WHEAT)
+1.000000 AverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0.0

AverageScenario_c_u_ConstrainTotalAcreage_:
+1.000000 AverageScenario_DevotedAcreage(CORN)
+1.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AverageScenario_DevotedAcreage(WHEAT)
<= 500.0

AverageScenario_c_e_ComputeFirstStageCost_:
-230.000000 AverageScenario_DevotedAcreage(CORN)
-260.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
-150.000000 AverageScenario_DevotedAcreage(WHEAT)
+1.000000 AverageScenario_FirstStageCost
= 0.0

AverageScenario_c_l_COMPUTE_SCENARIO_EXCESS_:
+1.000000 AverageScenario_CVAR_ETA
+1.000000 AverageScenario_CVAR_EXCESS
-1.000000 AverageScenario_FirstStageCost
-1.000000 AverageScenario_SecondStageCost
>= 0.0

AverageScenario_c_l_EnforceQuotas(CORN)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(CORN)
>= 0.0

AverageScenario_c_u_EnforceQuotas(CORN)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(CORN)
<= 100000.0

AverageScenario_c_l_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0.0

AverageScenario_c_u_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000.0

AverageScenario_c_l_EnforceQuotas(WHEAT)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0.0

AverageScenario_c_u_EnforceQuotas(WHEAT)_:
+1.000000 AverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000.0

AverageScenario_c_l_EnforceCattleFeedRequirement(CORN)_:
+3.000000 AverageScenario_DevotedAcreage(CORN)
+1.000000 AverageScenario_QuantityPurchased(CORN)
-1.000000 AverageScenario_QuantitySubQuotaSold(CORN)
-1.000000 AverageScenario_QuantitySuperQuotaSold(CORN)
>= 240.0

AverageScenario_c_l_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+20.000000 AverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AverageScenario_QuantityPurchased(SUGAR_BEETS)
-1.000000 AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1.000000 AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0.0

AverageScenario_c_l_EnforceCattleFeedRequirement(WHEAT)_:
+2.500000 AverageScenario_DevotedAcreage(WHEAT)
+1.000000 AverageScenario_QuantityPurchased(WHEAT)
-1.000000 AverageScenario_QuantitySubQuotaSold(WHEAT)
-1.000000 AverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200.0

AverageScenario_c_e_ONE_VAR_CONSTANT: 
AverageScenario_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario AverageScenario

\ Begin constraint block for scenario BelowAverageScenario
BelowAverageScenario_c_e_ComputeSecondStageCost_:
-210.000000 BelowAverageScenario_QuantityPurchased(CORN)
-100000.000000 BelowAverageScenario_QuantityPurchased(SUGAR_BEETS)
-238.000000 BelowAverageScenario_QuantityPurchased(WHEAT)
+150.000000 BelowAverageScenario_QuantitySubQuotaSold(CORN)
+36.000000 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+170.000000 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
+0.000000 BelowAverageScenario_QuantitySuperQuotaSold(CORN)
+10.000000 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
+0.000000 BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)
+1.000000 BelowAverageScenario_SecondStageCost
= 0.0

BelowAverageScenario_c_u_LimitAmountSold(CORN)_:
-2.400000 BelowAverageScenario_DevotedAcreage(CORN)
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(CORN)
+1.000000 BelowAverageScenario_QuantitySuperQuotaSold(CORN)
<= 0.0

BelowAverageScenario_c_u_LimitAmountSold(SUGAR_BEETS)_:
-16.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1.000000 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0.0

BelowAverageScenario_c_u_LimitAmountSold(WHEAT)_:
-2.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
+1.000000 BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0.0

BelowAverageScenario_c_u_ConstrainTotalAcreage_:
+1.000000 BelowAverageScenario_DevotedAcreage(CORN)
+1.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
<= 500.0

BelowAverageScenario_c_e_ComputeFirstStageCost_:
-230.000000 BelowAverageScenario_DevotedAcreage(CORN)
-260.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
-150.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
+1.000000 BelowAverageScenario_FirstStageCost
= 0.0

BelowAverageScenario_c_l_COMPUTE_SCENARIO_EXCESS_:
+1.000000 BelowAverageScenario_CVAR_ETA
+1.000000 BelowAverageScenario_CVAR_EXCESS
-1.000000 BelowAverageScenario_FirstStageCost
-1.000000 BelowAverageScenario_SecondStageCost
>= 0.0

BelowAverageScenario_c_l_EnforceQuotas(CORN)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(CORN)
>= 0.0

BelowAverageScenario_c_u_EnforceQuotas(CORN)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(CORN)
<= 100000.0

BelowAverageScenario_c_l_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0.0

BelowAverageScenario_c_u_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000.0

BelowAverageScenario_c_l_EnforceQuotas(WHEAT)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0.0

BelowAverageScenario_c_u_EnforceQuotas(WHEAT)_:
+1.000000 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000.0

BelowAverageScenario_c_l_EnforceCattleFeedRequirement(CORN)_:
+2.400000 BelowAverageScenario_DevotedAcreage(CORN)
+1.000000 BelowAverageScenario_QuantityPurchased(CORN)
-1.000000 BelowAverageScenario_QuantitySubQuotaSold(CORN)
-1.000000 BelowAverageScenario_QuantitySuperQuotaSold(CORN)
>= 240.0

BelowAverageScenario_c_l_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+16.000000 BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 BelowAverageScenario_QuantityPurchased(SUGAR_BEETS)
-1.000000 BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1.000000 BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0.0

BelowAverageScenario_c_l_EnforceCattleFeedRequirement(WHEAT)_:
+2.000000 BelowAverageScenario_DevotedAcreage(WHEAT)
+1.000000 BelowAverageScenario_QuantityPurchased(WHEAT)
-1.000000 BelowAverageScenario_QuantitySubQuotaSold(WHEAT)
-1.000000 BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200.0

BelowAverageScenario_c_e_ONE_VAR_CONSTANT: 
BelowAverageScenario_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario BelowAverageScenario

\ Begin constraint block for scenario AboveAverageScenario
AboveAverageScenario_c_e_ComputeSecondStageCost_:
-210.000000 AboveAverageScenario_QuantityPurchased(CORN)
-100000.000000 AboveAverageScenario_QuantityPurchased(SUGAR_BEETS)
-238.000000 AboveAverageScenario_QuantityPurchased(WHEAT)
+150.000000 AboveAverageScenario_QuantitySubQuotaSold(CORN)
+36.000000 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+170.000000 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
+0.000000 AboveAverageScenario_QuantitySuperQuotaSold(CORN)
+10.000000 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
+0.000000 AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)
+1.000000 AboveAverageScenario_SecondStageCost
= 0.0

AboveAverageScenario_c_u_LimitAmountSold(CORN)_:
-3.600000 AboveAverageScenario_DevotedAcreage(CORN)
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(CORN)
+1.000000 AboveAverageScenario_QuantitySuperQuotaSold(CORN)
<= 0.0

AboveAverageScenario_c_u_LimitAmountSold(SUGAR_BEETS)_:
-24.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
+1.000000 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
<= 0.0

AboveAverageScenario_c_u_LimitAmountSold(WHEAT)_:
-3.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
+1.000000 AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)
<= 0.0

AboveAverageScenario_c_u_ConstrainTotalAcreage_:
+1.000000 AboveAverageScenario_DevotedAcreage(CORN)
+1.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
<= 500.0

AboveAverageScenario_c_e_ComputeFirstStageCost_:
-230.000000 AboveAverageScenario_DevotedAcreage(CORN)
-260.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
-150.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
+1.000000 AboveAverageScenario_FirstStageCost
= 0.0

AboveAverageScenario_c_l_COMPUTE_SCENARIO_EXCESS_:
+1.000000 AboveAverageScenario_CVAR_ETA
+1.000000 AboveAverageScenario_CVAR_EXCESS
-1.000000 AboveAverageScenario_FirstStageCost
-1.000000 AboveAverageScenario_SecondStageCost
>= 0.0

AboveAverageScenario_c_l_EnforceQuotas(CORN)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(CORN)
>= 0.0

AboveAverageScenario_c_u_EnforceQuotas(CORN)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(CORN)
<= 100000.0

AboveAverageScenario_c_l_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
>= 0.0

AboveAverageScenario_c_u_EnforceQuotas(SUGAR_BEETS)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
<= 6000.0

AboveAverageScenario_c_l_EnforceQuotas(WHEAT)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
>= 0.0

AboveAverageScenario_c_u_EnforceQuotas(WHEAT)_:
+1.000000 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
<= 100000.0

AboveAverageScenario_c_l_EnforceCattleFeedRequirement(CORN)_:
+3.600000 AboveAverageScenario_DevotedAcreage(CORN)
+1.000000 AboveAverageScenario_QuantityPurchased(CORN)
-1.000000 AboveAverageScenario_QuantitySubQuotaSold(CORN)
-1.000000 AboveAverageScenario_QuantitySuperQuotaSold(CORN)
>= 240.0

AboveAverageScenario_c_l_EnforceCattleFeedRequirement(SUGAR_BEETS)_:
+24.000000 AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)
+1.000000 AboveAverageScenario_QuantityPurchased(SUGAR_BEETS)
-1.000000 AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)
-1.000000 AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)
>= 0.0

AboveAverageScenario_c_l_EnforceCattleFeedRequirement(WHEAT)_:
+3.000000 AboveAverageScenario_DevotedAcreage(WHEAT)
+1.000000 AboveAverageScenario_QuantityPurchased(WHEAT)
-1.000000 AboveAverageScenario_QuantitySubQuotaSold(WHEAT)
-1.000000 AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)
>= 200.0

AboveAverageScenario_c_e_ONE_VAR_CONSTANT: 
AboveAverageScenario_ONE_VAR_CONSTANT = 1.0

\ End constraint block for scenario AboveAverageScenario

bounds

\ Begin variable bounds block for master
     -inf <=  MASTER_AboveAverageNode_SecondStageCost  <= +inf
     -inf <=  MASTER_AverageNode_SecondStageCost  <= +inf
     -inf <=  MASTER_BelowAverageNode_SecondStageCost  <= +inf
     -inf <=  MASTER_CVAR_COST_RootNode  <= +inf
     -inf <=  MASTER_EXPECTED_COST_AboveAverageNode  <= +inf
     -inf <=  MASTER_EXPECTED_COST_AverageNode  <= +inf
     -inf <=  MASTER_EXPECTED_COST_BelowAverageNode  <= +inf
     -inf <=  MASTER_EXPECTED_COST_RootNode  <= +inf
     -inf <=  MASTER_RootNode_CVAR_ETA  <= +inf
     -inf <=  MASTER_RootNode_DevotedAcreage(CORN)  <= +inf
     -inf <=  MASTER_RootNode_DevotedAcreage(SUGAR_BEETS)  <= +inf
     -inf <=  MASTER_RootNode_DevotedAcreage(WHEAT)  <= +inf
     -inf <=  MASTER_RootNode_FirstStageCost  <= +inf
\ End variable bounds block for master

\ Begin variable bounds block for scenario AverageScenario
     -inf <=  AverageScenario_CVAR_ETA  <= +inf
    0 <=  AverageScenario_CVAR_EXCESS  <= +inf
    0.0 <=  AverageScenario_DevotedAcreage(CORN)  <= 500
    0.0 <=  AverageScenario_DevotedAcreage(SUGAR_BEETS)  <= 500
    0.0 <=  AverageScenario_DevotedAcreage(WHEAT)  <= 500
     -inf <=  AverageScenario_FirstStageCost  <= +inf
    0.0 <=  AverageScenario_QuantityPurchased(CORN)  <= +inf
    0.0 <=  AverageScenario_QuantityPurchased(SUGAR_BEETS)  <= +inf
    0.0 <=  AverageScenario_QuantityPurchased(WHEAT)  <= +inf
    0.0 <=  AverageScenario_QuantitySubQuotaSold(CORN)  <= +inf
    0.0 <=  AverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  AverageScenario_QuantitySubQuotaSold(WHEAT)  <= +inf
    0.0 <=  AverageScenario_QuantitySuperQuotaSold(CORN)  <= +inf
    0.0 <=  AverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  AverageScenario_QuantitySuperQuotaSold(WHEAT)  <= +inf
     -inf <=  AverageScenario_SecondStageCost  <= +inf
\ End variable bounds block for scenario AverageScenario

\ Begin variable bounds block for scenario BelowAverageScenario
     -inf <=  BelowAverageScenario_CVAR_ETA  <= +inf
    0 <=  BelowAverageScenario_CVAR_EXCESS  <= +inf
    0.0 <=  BelowAverageScenario_DevotedAcreage(CORN)  <= 500
    0.0 <=  BelowAverageScenario_DevotedAcreage(SUGAR_BEETS)  <= 500
    0.0 <=  BelowAverageScenario_DevotedAcreage(WHEAT)  <= 500
     -inf <=  BelowAverageScenario_FirstStageCost  <= +inf
    0.0 <=  BelowAverageScenario_QuantityPurchased(CORN)  <= +inf
    0.0 <=  BelowAverageScenario_QuantityPurchased(SUGAR_BEETS)  <= +inf
    0.0 <=  BelowAverageScenario_QuantityPurchased(WHEAT)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySubQuotaSold(CORN)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySubQuotaSold(WHEAT)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySuperQuotaSold(CORN)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  BelowAverageScenario_QuantitySuperQuotaSold(WHEAT)  <= +inf
     -inf <=  BelowAverageScenario_SecondStageCost  <= +inf
\ End variable bounds block for scenario BelowAverageScenario

\ Begin variable bounds block for scenario AboveAverageScenario
     -inf <=  AboveAverageScenario_CVAR_ETA  <= +inf
    0 <=  AboveAverageScenario_CVAR_EXCESS  <= +inf
    0.0 <=  AboveAverageScenario_DevotedAcreage(CORN)  <= 500
    0.0 <=  AboveAverageScenario_DevotedAcreage(SUGAR_BEETS)  <= 500
    0.0 <=  AboveAverageScenario_DevotedAcreage(WHEAT)  <= 500
     -inf <=  AboveAverageScenario_FirstStageCost  <= +inf
    0.0 <=  AboveAverageScenario_QuantityPurchased(CORN)  <= +inf
    0.0 <=  AboveAverageScenario_QuantityPurchased(SUGAR_BEETS)  <= +inf
    0.0 <=  AboveAverageScenario_QuantityPurchased(WHEAT)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySubQuotaSold(CORN)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySubQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySubQuotaSold(WHEAT)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySuperQuotaSold(CORN)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySuperQuotaSold(SUGAR_BEETS)  <= +inf
    0.0 <=  AboveAverageScenario_QuantitySuperQuotaSold(WHEAT)  <= +inf
     -inf <=  AboveAverageScenario_SecondStageCost  <= +inf
\ End variable bounds block for scenario AboveAverageScenario

end
