import sys, os
import shutil
import time
import pexpect

def pretty_print(info, printHeader):

  data = info['History']

  start = data[0]
  end = data[-1]
  profit = end - start
  days = len(data)

  p_per_year = 0
  percents = 0
  years = float(days) / 200

  if profit > 0:
    percents = (100.0 * float(profit)) / start  
    p_per_year = percents / years

  
  maxV = max(data)
  minV = min(data)

  fname = info['Data file']
  if fname.endswith('.stocks'):
    fname = fname[: -len('.stocks')]

  def floatFormat(f):
    return'%.5f' % f

  columns = ('File'  , 'Initial', 'Ending', 'Profit', 'Days', 'Percent/y', 'Profit/y'    )
  values =  [fname   , start    , end     , profit  ,  days,  floatFormat(percents / years),  floatFormat (float(profit) / years)  ]
  formatted = tuple([str(e) for e in values])

  fs = [ '%18.18s ']
  for i in range(0, len(columns) - 1):
    fs.append('%12.12s')

  fs = " ".join(fs)

  if printHeader:
    print ( fs % columns)

  print ( fs % formatted)


def message_loop(exe, logfileName, msgProcessing):
  l = open(logfileName, "w")
  def log(a, m):
     l.write("[%s] : %s\n" % (a, m.strip()))

  EMULATOR = "emulator"
  TRADER = "trader"

  p = pexpect.spawn("./" + exe)
  p.delaybeforesend = None
  p.setecho(False)
  
  def send(msg):
      log(EMULATOR, msg)
      p.sendline(msg) 
  
  def receive():    
      y = p.readline().decode()
      log(TRADER, y)
      return y

  response = None
  state = None
  while True:
    msg, state = msgProcessing(response, state)
    if not isinstance(msg, str):
        break

    send(msg)
    response = receive()

  info = msg
  l.close()

  return info


def createMsgProcessor(dataname, data, money):
    days = len(data)

    def add(state, name, amount):
        state[name] = state[name] + amount

    def incDay(state):
        add(state, 'day', 1)
        
    def addMoney(state, amount):
        add(state, 'money', amount)

    def addStock(state, amount):
        add(state, 'stock', amount)
  
    def processor(msg, state):      
        if not state:
          state = {'day' : 0, 'money' : money, 'stock' : 0, 'history' : [money]}
        
        if msg == None:
            return ("Exchange opened for %d days. Initial money = %d" % (days, money), state)

        if msg.strip() == "OK":
            curDay = state['day']
            assert curDay == 0
            return ("%d %d %d" % (data[curDay], state['money'], state['stock']), state)

        order, amount = msg.split(' ')
        assert order.strip() in ['Buy', 'Sell']
        amount = int(amount)
        expense = amount * data[state['day']]

        if order == "Sell":
            if amount > state['stock']:
                print ("Trying to sell more stocks than actually have")
                exit()
            else:
                addStock(state, -amount)
                addMoney(state, expense)

        if order == "Buy":         
            if expense > state['money']:
                print ("Trying to buy for more money than actually have")
                exit()
            else:
                addStock(state, amount)
                addMoney(state, -expense)

        moneyHistory = state['history']
        moneyHistory.append(state['money'])
        incDay(state)
        day = state['day']

        if day == days:
            return ({'Data file'       : dataname,
                     'History'         : moneyHistory
                     },
                     state
                     )

        return ("%d %d %d" % (data[day], state['money'], state['stock']), state)


    return processor

if __name__=='__main__':
    if not len(sys.argv) in [5, 6]:
        print("Usage: python emulator file.stock binary initialMoney tmpDir")
        print("Usage: python emulator -no-header file.stock binary initialMoney tmpDir")
        exit()
    
    noHead = False

    if sys.argv[1] == '-no-header':
       sys.argv[1:] = sys.argv[2:]
       noHead = True

    stocks = sys.argv[1] 
    binary = sys.argv[2]
    initialMoney = int(sys.argv[3])
    tmp = sys.argv[4]
  
    #print('Running %s with input %s. InitialMoney = %d' % (binary, stocks, initialMoney))

    TMP_DIR = tmp
    testedBin = "trader.bin"
    testedData = "data.stocks"

    #print("Removing %s" % TMP_DIR)
    shutil.rmtree(TMP_DIR, ignore_errors=True)

    #print("Creating %s" % TMP_DIR)
    os.mkdir(TMP_DIR)

    t = os.path.join(TMP_DIR,  testedBin)
    #print("Copy %s to %s" % (binary, t))
    shutil.copy(binary, t)

    t = os.path.join(TMP_DIR,  testedData)
    #print("Copy %s to %s" % (stocks, t))
    shutil.copyfile(stocks, t)

    os.chdir(TMP_DIR)

    data = [ int(x) for x in open(testedData, "r") if not x.startswith("#")]

    info = message_loop(testedBin, testedBin + ".log", createMsgProcessor(stocks, data, initialMoney))

    pretty_print(info, not noHead)
  
