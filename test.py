from GQLib.Framework import Framework
from GQLib.Optimizers import MPGA, PSO, SGA, SA, NELDER_MEAD, TABU, FA
from GQLib.Models import LPPL, LPPLS
from GQLib.enums import InputType
from GQLib.AssetProcessor import AssetProcessor
import numpy as np




wti = AssetProcessor(input_type = InputType.WTI)

try:
    wti.generate_all_rectangle(frequency = "daily",
                            optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                            significativity_tc=0.3,
                            rerun = True,
                            nb_tc = 10,
                            save=True,
                            save_plot=True)
except:
    pass

try:
    wti.generate_all_rectangle(frequency = "daily",
                            optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                            significativity_tc=0.3,
                            rerun = True,
                            nb_tc = 10,
                            save=True,
                            save_plot=True)
except:
    pass

try:
    wti.generate_all_rectangle(frequency = "weekly",
                            optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                            significativity_tc=0.3,
                            rerun = True,
                            nb_tc = 10,
                            save=True,
                            save_plot=True)
except:
    pass

try:
    wti.generate_all_rectangle(frequency = "weekly",
                        optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

sp500 = AssetProcessor(input_type = InputType.SP500)

try:
    sp500.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

try:
    sp500.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

try:
    sse = AssetProcessor(input_type = InputType.SSE)
except:
    pass

try:
    sse.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

try:
    sse.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass


try:
    uso = AssetProcessor(input_type = InputType.USO)
except:
    pass

try:
    uso.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

try:
    uso.generate_all_rectangle(frequency = "daily",
                        optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass

try:
    uso.generate_all_rectangle(frequency = "weekly",
                            optimizers =  [SA(LPPL), SGA(LPPL), NELDER_MEAD(LPPLS), TABU(LPPL), FA(LPPL), MPGA(LPPL), PSO(LPPL)], 
                            significativity_tc=0.3,
                            rerun = True,
                            nb_tc = 10,
                            save=True,
                            save_plot=True)
except:
    pass

try:
    uso.generate_all_rectangle(frequency = "weekly",
                        optimizers =  [SA(LPPLS), SGA(LPPLS), NELDER_MEAD(LPPLS), TABU(LPPLS), FA(LPPLS), MPGA(LPPLS), PSO(LPPLS)], 
                        significativity_tc=0.3,
                        rerun = True,
                        nb_tc = 10,
                        save=True,
                        save_plot=True)
except:
    pass