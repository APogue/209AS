## PSET2 
MDP value iteration and policy iteration to get to a goal state in Gridworld. The agent can move forwards and backwards with turning constraints.
#### Rewards
* Red square: -100
* Yellow square: -10
* White square: 0
* Green square: varying positive reward
#### Other parameters
* States: 6x6 grid, 12 heading angles
* Actions: none, forwards, backwards, forwards left, forwards right, backwards left, backwards right
* Discount factor: .9
* Error probability: .25


### Initial policy
Designed to get to the green block in a minimum number of moves, without regard for reward
<object data="https://github.com/APogue/209AS/blob/master/PSET2/images/Initial%20Policy%20Trajectoryssssssssss.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="http://yoursite.com/the.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/APogue/209AS/blob/master/PSET2/images/Initial%20Policy%20Trajectoryssssssssss.pdf">Download PDF</a>.</p>
    </embed>
</object>

### Policy Iteration 
Green square reward: 100 

<object data="https://github.com/APogue/209AS/blob/master/PSET2/images/PolicyOptimalTrajectoryGoals_allllll.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="http://yoursite.com/the.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/APogue/209AS/blob/master/PSET2/images/PolicyOptimalTrajectoryGoals_allllll.pdf">Download PDF</a>.</p>
    </embed>
</object>

Green square reward: 250, only rewarded if agent heading is 6 o'clock

<object data="https://github.com/APogue/209AS/blob/master/PSET2/images/PolicyOptimalTrajectoryGoals.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="http://yoursite.com/the.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/APogue/209AS/blob/master/PSET2/images/PolicyOptimalTrajectoryGoals.pdf">Download PDF</a>.</p>
    </embed>
</object>

### Value Iteration
Green square reward: 350, only rewarded if agent heading is 6 o'clock

<object data="https://github.com/APogue/209AS/blob/master/PSET2/images/ValueIterationTrajectoryGoalsblaaaa.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="https://github.com/APogue/209AS/blob/master/PSET2/images/ValueIterationTrajectoryGoalsblaaaa.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="https://github.com/APogue/209AS/blob/master/PSET2/images/ValueIterationTrajectoryGoalsblaaaa.pdf">Download PDF</a>.</p>
    </embed>
</object>

