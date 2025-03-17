from py3dbp import Packer, Bin, Item, Painter
import random
import time
start = time.time()


#  init bin 
container = Bin('HQ Container 40 Feets', (1200, 235, 269), 304800000,0,1)

# Data boxes
raw_items = [
    {"id": 1, "name": "40019FF0002A6", "w": 113, "h": 91, "d": 32, "weight": 82300, "count": 25, "priority": 1, "updown": True, "type": "cube"},
    {"id": 2, "name": "40018FF0001C1", "w": 113, "h": 93, "d": 32, "weight": 73600, "count": 20, "priority": 1, "updown": True, "type": "cube"},
    {"id": 3, "name": "40021FF0009C3", "w": 115, "h": 103, "d": 32, "weight": 77000, "count": 130, "priority": 1, "updown": True, "type": "cube"},
    {"id": 4, "name": "122015FF002A4", "w": 17, "h": 5, "d": 10, "weight": 6120, "count": 2, "priority": 2, "updown": True, "type": "cube"},
    {"id": 5, "name": "142819FF0000A1", "w": 40, "h": 30, "d": 20, "weight": 2160, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 6, "name": "211015FF0001A4", "w": 15, "h": 15, "d": 15, "weight": 1390, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 7, "name": "4220-FF1001-001", "w": 12, "h": 10, "d": 30, "weight": 10600, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 8, "name": "422922FF000001", "w": 19, "h": 7, "d": 24, "weight": 825, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 9, "name": "423015FF0003A1", "w": 19, "h": 7, "d": 24, "weight": 1440, "count": 20, "priority": 2, "updown": True, "type": "cube"},
    {"id": 10, "name": "442818FF0004A6", "w": 48, "h": 22, "d": 30, "weight": 500, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 11, "name": "4552-TW0200-001", "w": 80, "h": 20, "d": 30, "weight": 1300, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 12, "name": "4710-SD001S-001", "w": 20, "h": 15, "d": 20, "weight": 6500, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 13, "name": "4710-SD001S-001", "w": 30, "h": 15, "d": 20, "weight": 26000, "count": 2, "priority": 2, "updown": True, "type": "cube"},
    {"id": 14, "name": "4710-VL4423-001", "w": 30, "h": 15, "d": 20, "weight": 12800, "count": 5, "priority": 2, "updown": True, "type": "cube"},
    {"id": 15, "name": "472915FF0004A8", "w": 30, "h": 30, "d": 25, "weight": 2600, "count": 1, "priority": 2, "updown": True, "type": "cube"},
    {"id": 16, "name": "472924FF000001", "w": 26, "h": 9, "d": 19, "weight": 900, "count": 1, "priority": 2, "updown": True, "type": "cube"},
]


items = []
for item in raw_items:
    items.extend([item] * item["count"])
    
items.sort(key=lambda item: (item["w"] * item["h"] * item["d"], item["weight"]), reverse=True)

packer = Packer()
packer.addBin(container)


# Item('item partno', (W,H,D), Weight, Packing Priority level, load bear, Upside down or not , 'item color')
for item in items:
  packer.addItem(
      Item(
          partno=item['id'], 
          name=item['name'], 
          typeof=item['type'], 
          WHD=(item['w'], item['h'], item['d']), 
          weight=item['weight'], 
          level=item['priority'],
          loadbear=100, 
          updown=item['updown'], 
          color="#{:06x}".format(random.randint(0, 0xFFFFFF))
          )
      )


# calculate packing 
packer.pack(
    bigger_first=True,
    distribute_items=True,
    fix_point=True,
    check_stable=True,
    support_surface_ratio=0.5,
    number_of_decimals=0
)

# put order
packer.putOrder()

# print result
b = packer.bins[0]
volume = b.width * b.height * b.depth
print(":::::::::::", b.string())

print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''
for item in b.items:
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("position : ",item.position)
    print("rotation type : ",item.rotation_type)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_t += float(item.width) * float(item.height) * float(item.depth)
    print("***************************************************")
print("***************************************************")
print("UNFITTED ITEMS:")
for item in b.unfitted_items:
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
    print("volume : ",float(item.width) * float(item.height) * float(item.depth))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.depth)
    unfitted_name += '{},'.format(item.partno)
    print("***************************************************")
print("***************************************************")
print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
print('residual volume : ', float(volume) - volume_t )
print('pack item count : ', b.items.__len__())
print('unpack item : ',unfitted_name)
print('unpack item count : ',b.unfitted_items.__len__())
print('unpack item volume : ',volume_f)
print("gravity distribution : ",b.gravity)
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
fig = painter.plotBoxAndItems(
    title=b.partno,
    alpha=0.6,
    write_num=False,
    fontsize=10
)
fig.show()