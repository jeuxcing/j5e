from j5e.game.Timer import Timer
from j5e.game.Agents import Lemming, Trap

if __name__ == "__main__":
    #stopFlag = Event()
    #timer = Timer(stopFlag)
    timer = Timer()
    timer.add(Lemming(1, "Lemmiwings",0, 5,1))
    #timer.add(Lemming(2, "Octodon",7, 4,-1))
    #timer.add(Trap(3, "une porte",4))
       
    timer.start()
    
    #String, int, int, int, int
    #type, x, y, num, dir
    #LED,0,0,0,1
    
