import numpy as np
from box import BoundBox

#OVERLAP
def overlap_c(x1, w1, x2, w2):
    #float l1,l2,left,right
    l1 = x1 - w1 /2.
    l2 = x2 - w2 /2.
    left = max(l1,l2)
    r1 = x1 + w1 /2.
    r2 = x2 + w2 /2.
    right = min(r1, r2)
    return right - left;

#BOX INTERSECTION
def box_intersection_c(ax, ay, aw, ah, bx, by, bw, bh):
    #float w,h,area
    w = overlap_c(ax, aw, bx, bw)
    h = overlap_c(ay, ah, by, bh)
    if w < 0 or h < 0: return 0
    area = w * h
    return area

#BOX UNION
def box_union_c(ax, ay, aw, ah, bx, by, bw, bh):
    #float i,u
    i = box_intersection_c(ax, ay, aw, ah, bx, by, bw, bh)
    u = aw * ah + bw * bh -i
    return u


#BOX IOU
def box_iou_c(ax, ay, aw, ah, bx, by, bw, bh):
    return box_intersection_c(ax, ay, aw, ah, bx, by, bw, bh) / box_union_c(ax, ay, aw, ah, bx, by, bw, bh);




#NMS
def NMS(final_probs , final_bbox):
    boxes = list()
    indices = set()
    #np.intp_t pred_length,class_length,class_loop,index,index2

  
    pred_length = final_bbox.shape[0]
    class_length = final_probs.shape[1]
    for class_loop in range(class_length):
        for index in range(pred_length):
            if final_probs[index,class_loop] == 0: continue
            for index2 in range(index+1,pred_length):
                if final_probs[index2,class_loop] == 0: continue
                if index==index2 : continue
                if box_iou_c(final_bbox[index,0],final_bbox[index,1],final_bbox[index,2],final_bbox[index,3],final_bbox[index2,0],final_bbox[index2,1],final_bbox[index2,2],final_bbox[index2,3]) >= 0.4:
                    if final_probs[index2,class_loop] > final_probs[index, class_loop] :
                        final_probs[index, class_loop] =0
                        break
                    final_probs[index2,class_loop]=0
            
            if index not in indices:
                bb=BoundBox(class_length)
                bb.x = final_bbox[index, 0]
                bb.y = final_bbox[index, 1]
                bb.w = final_bbox[index, 2]
                bb.h = final_bbox[index, 3]
                bb.c = final_bbox[index, 4]
                bb.probs = np.asarray(final_probs[index,:])
                boxes.append(bb)
                indices.add(index)
    return boxes

# cdef NMS(float[:, ::1] final_probs , float[:, ::1] final_bbox):
#     cdef list boxes = list()
#     cdef:
#         np.intp_t pred_length,class_length,class_loop,index,index2, i, j

  
#     pred_length = final_bbox.shape[0]
#     class_length = final_probs.shape[1]

#     for class_loop in range(class_length):
#         order = np.argsort(final_probs[:,class_loop])[::-1]
#         # First box
#         for i in range(pred_length):
#             index = order[i]
#             if final_probs[index, class_loop] == 0.: 
#                 continue
#             # Second box
#             for j in range(i+1, pred_length):
#                 index2 = order[j]
#                 if box_iou_c(
#                     final_bbox[index,0],final_bbox[index,1],
#                     final_bbox[index,2],final_bbox[index,3],
#                     final_bbox[index2,0],final_bbox[index2,1],
#                     final_bbox[index2,2],final_bbox[index2,3]) >= 0.4:
#                     final_probs[index2, class_loop] = 0.
                    
#             bb = BoundBox(class_length)
#             bb.x = final_bbox[index, 0]
#             bb.y = final_bbox[index, 1]
#             bb.w = final_bbox[index, 2]
#             bb.h = final_bbox[index, 3]
#             bb.c = final_bbox[index, 4]
#             bb.probs = np.asarray(final_probs[index,:])
#             boxes.append(bb)
  
#     return boxes
