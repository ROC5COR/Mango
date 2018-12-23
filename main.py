import sys
import mango
import utils

#######MAIN#######
mango.init()
print("Mango v"+str(mango.mango_version))

if len(sys.argv) > 1: # An arguments was passed
    print(sys.argv[1])
    if sys.argv[1] == '--all' or sys.argv[1] == '-a' or sys.argv[1] == 'all' :
        mango.show_all_plugin()
        print("Mango in plate")
    elif sys.argv[1] == '-s' or sys.argv[1] == '--server':
        mango.start_server()
    elif sys.argv[1] == '-i' or sys.argv[1] == '--interactive':
        while(True):
            try:
                user_input = str(input("[MANGO] > ")).strip()
                user_inputs = user_input.split(' ') # TODO change to manage '"' that make sub-strings
                (result,message) = mango.parse_command(user_inputs)
                if result == 0:
                    break
            except KeyboardInterrupt:
                print("Exiting")
                break
    else:
        if mango.parse_command(sys.argv[1:]) < 0:
            print("Rotten mango !")
        else:
            print("Mango in plate")

else:
    mango.show_normal_plugin()
    print("Mango in plate")




