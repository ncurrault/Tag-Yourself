/newgraph _name_
Create a new graph with the given title. Graphs are initially 0-dimensional and empty.
*Example message*:
```
/newgraph Healing
```

/addaxis _name_ _axis label_
Add an axis to a graph. Any existing points will be plotted at 0 on the new axis.
*Example messages*:
```
/addaxis emotional healing
/addaxis physical healing
```

/listaxes _name_
Lists a graph's axes in the order that coordinates are expected.
*Example message*:
```
/listaxes Healing
```

/lookatthisgraph _name_
Display a graph
*Example message*:
```
/lookatthisgraph Healing
```

/tag _name_ _coordinates_ [ _point label_ ]
Add a point to a graph. Use caller's Telegram name initials if no provided label.
All axes in all graphs are on the scale \[-1, 1]

*Example message*:
```
/tag Healing (-1, -1) bad
/tag Healing (1, 1) good
```
