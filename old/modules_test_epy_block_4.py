"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class my_basic_adder_block(gr.basic_block):
    # def __init__(self):
    #     gr.basic_block.__init__(self,
    #         name="test_blqsdock",
    #         in_sig=[np.uint8],
    #         out_sig=[np.uint8])

    # def forecast(self, noutput_items, ninputs) :
    #     ninput_items_required = [0]*ninputs #ninput_items_required[i] is the number of items that will be consumed on input port i
    #     for i in range(ninputs):
    #         ninput_items_required[i] = 1.5 * noutput_items * ninputs

    #     # print("--- FORECAST ---")
    #     # print(ninputs)
    #     # print(noutput_items)
    #     # print(ninput_items_required)

    #     return ninput_items_required


    # def general_work(self, input_items, output_items):
        
    #     #buffer references
    #     in0 = input_items[0][:len(output_items[0])]
    #     out = output_items[0]
        

    #     output_items[0][:] = in0


    #     print("\n--- GENERAL WORK 1  ---")
    #     print("input_items[0]")
    #     print(input_items[0])
    #     print("in0")
    #     print(in0)
    #     print("len(in0)")
    #     print(len(in0))
    #     print("output_items[0]")
    #     print(output_items[0])
    #     print("len(output_items[0])")
    #     print(len(output_items[0]))

    #     #consume the inputs
    #     self.consume(0, len(in0)) #consume port 0 input
    #     # self.produce(0, 1) #produce 3 items on port 0
    #     #return produced
    #     return len(output_items[0])

   def __init__(self, input_buffer_len=2):
      gr.basic_block.__init__(self,
         name="sync_test",
         in_sig=[np.uint8],
         out_sig=[np.uint8])
      self.input_buffer_len = input_buffer_len

   def forecast(self, noutput_items, ninputs):
    #   print("FORECAST START")
      ninput_items_required = [self.input_buffer_len] * ninputs
    #   print("len(ninput_items_required),noutput_items",len(ninput_items_required),noutput_items)
    #   print("FORECAST END")
      return ninput_items_required

   def general_work(self, input_items, output_items):
    print("\n--- GENERAL WORK START ---")
    if(len(input_items[0]) >= self.input_buffer_len) :
        out_vect = [0xFF, 0x55, 0xAA]
        output_items[0][0:len(out_vect)] = out_vect
        self.consume(0, self.input_buffer_len)
        self.produce(0, len(out_vect))


        print("len(input_items)", len(input_items[0]))
        print("input_buffer_len", self.input_buffer_len)
        print("len(input_items[0]) >= input_buffer_len")
        print("len(output_items[0])", len(output_items[0]))
        print("output_items[0] = ")
        print(output_items[0])

    print("--- GENERAL WORK END ---")
    return len(out_vect)