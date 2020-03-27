# distBrute
## A gobuster wrapper for the distributed minded person

I like to use gobuster but then I find it annoying to have to manually re-run if I want to do deeper level sub-domain bruteforcing. The idea is to make use of AWS ec2 instnaces and the concept of distributed computing to speed things up and most importantly, not manually re-run command everytime. 


### Advantanges
There are couple of advantages to run bruteforcer on a so-called distributed system:
1. If you get IP blocked you can easily spin up a new box
2. Theoretically there is no limit on how many bruteforcer you can run at the same time, meaning you can do stuff truly concurrently
3. You don't have to manually type the gobuster command by hand


### How it works? (Subject to change since this is still a work in prog)

