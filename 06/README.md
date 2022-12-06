# [Day 6: Tuning Trouble](https://adventofcode.com/2022/day/6)

Done in Google Sheets (because I was on mobile only today),
splitting the inputs into rows (using `mid(<inputcell>, row(), 1)`),
and then using the `countunique` function over the previous 4 or 14 cells
and then getting the minimum row number where the unique count equals 4 or 14.
