Joy
===

Joy from Inside Out. How is your team's morale? She'll let you know!

* @joy get morale - gets overall morale of team
* @joy get morale [user] - gets morale of [user]
* @joy get morale [channel] - gets morale of channel

Joy will also privately check in with those who are feeling down. 

<a href="https://slack.com/oauth/authorize?scope=incoming-webhook,bot&client_id=3378813695.19322733543"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>

Inspiration
===
*Inside Out* was a fantastic movie. The primary focus rested on the interplay of emotions within us and how this affected our behavior towards others. The physical plight of the main character, Riley, in a new and unfamiliar city takes a backseat to the intricate personification of her restless emotions within. In some ways, an organization is like Riley -- emotional stability within brings out the best externally. That's where Joy comes in; she serves as Riley's internal sidekick, and through additional bringing-to-life via Slackbot, she can be the emotional barometer of your organization.


Methodology
===

In channels that Joy is in, messages are analyzed in real-time by IBM Watson's tone analyzer. Watson provides values from 0 to 1 for nine subcategories in three main tone categories.

* Emotional Tone
	*  cheerfulness
	*  negative
	*  anger
* Writing Tone
	*  analytical
	*  confident
	*  tentative
* Social Tone
	*  openness
	*  agreeableness
	*  conscientiousness


Morale is calculated loosely based on the research done by Melany E. Baehr and Richard Renck in *The Definition and Measurement of Employee Morale*. Baehr and Renck identified five main factors that contribute to employee morale:

* Organization and Management (A)
* Immediate Supervision (B)
* Material Rewards (C)
* Fellow Employees (D)
* Job Satisfaction (E)

Of these five, I figured A, B, and D were measurable through tone data provided by Watson. Baehr and Renck computed the correlation between each factor and morale. I used this data as weights for each factor. For example, factor A was found to have the highest correlation with morale, so I weighted the score for factor A the heaviest.
