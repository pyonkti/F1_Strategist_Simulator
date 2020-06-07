---------------------------------------------------------------
The executable simulators are fastTeamLapTimeGenerator.py
and realTimeSimulator.py.

The initialization process is introduced in the paper section 4.6.

If you want to change the strategies of any one of the modeled
six drivers, go to \learn\tyre.csv. And follow these steps
- Search raceID for 1012
- Find the racer you want to change
- Alter his tyre and laps he goes through

*Be aware that Gasly does not have used medium tyre due to the rules!
----------------------------------------------------------------------------

In case you want to testify the drawings, the result are stored in
those folders if you notice.

If you want to draw these charts again, go to 
costOfOverlapping.py and costOfOvertaking.py first and decomment the
drawing part.

Those charts would be the distribution chart with y in numbers.
And they also deaw discrete chart of probability.

Then go to overtake.py and overlap.py. They will draw accumulated
probability charts and curve fit result.

*Be aware that costOfOverlapping.py may take some time
----------------------------------------------------------------------------------

The evaluation data shown in the paper is stored in \SimulationResult

Check it by running preset simulator (Will not written into those files, those are
stored manually).

----------------------------------------------------------------------------------

Charts stored in \Diagrams are not exactly the same with the papers
It was used temporarily.