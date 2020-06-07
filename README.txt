This file explains the structure of this directory

- presetSimulator.py (fast simulation for data analysis)
- realTimeSimulator.py (playable simulation for detailed information)
- costOfOverlapping.py (overlap raw data collection and print out)
- costOfOvertaking.py (overtake raw data collection and print out)
- overtake.py (advanced data modification and overlap modeling)
- overlap.py (advanced data modification and overtake modeling)
- fastTeamLapTimeGenerator.py (advanced data modification and lap time modeling)
- \learn (raw data)
---------------------------------------------------------------
The executable simulators are presetSimulator.py
and realTimeSimulator.py.

The initialization process is introduced 
in the paper section 4.6.

If you want to change the strategies of any one of the 
modeled six drivers, go to \learn\tyre.csv. And follow these steps
- Search raceID for 1012
- Find the racer you want to change
- Alter his tyre and laps he goes through

*Be aware that Gasly does not have used medium tyre 
due to the rules!
----------------------------------------------------------------------------

In case you want to testify the drawings, the result are stored in
those folders:
- \CostofBeingOvertook
-\CostofBeOverlapped
-\CostofOverlapping
-\CostofOvertaking
-\GapPossibility
-\LapTimeAdvPossibilty

If you want to draw these charts again, go to 
costOfOverlapping.py and costOfOvertaking.py 
It will both print out and save charts.

* Be aware that only Bar charts will be saved. 
The discret probability and accumulated probability for time cost would only be printed out

Then go to overtake.py and overlap.py. They will draw accumulated
probability charts and curve fitted result.

*Be aware that costOfOverlapping.py may take some time
----------------------------------------------------------------------------------

The evaluation data shown in the paper is stored in \SimulationResult

Check it by running preset simulator (Will not written into those files, those are
stored manually).

----------------------------------------------------------------------------------

Charts stored in \Diagrams are not exactly the same with the papers
It was used temporarily.