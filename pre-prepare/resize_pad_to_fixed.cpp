/*************************************************************************
    > File Name: resize_pad_to_fixed.cpp
    > Author: li_pengju
    > Mail: li_pengju@vobile.cn 
    > Copyright (c) Vobile Inc. All Rights Reserved
    > Created Time: 2017-12-06 16:09:13
 ************************************************************************/

#include<iostream>
#include<opencv2/opencv.hpp>

#define FIXED_H 416
#define FIXED_W 416

using namespace std;
using namespace cv;
int main(int argc, char *argv[])
{
    Mat srcIm = imread(argv[1], 1);
    if( srcIm.empty() ) {
        cout<<"Read "<<argv[1]<<" error !"<<endl;
        return -1;
    }
    cout<<"[height, width]: ["<<srcIm.rows<<", "<<srcIm.cols<<"]"<<endl;

    int newW, newH;
    Mat dst;
    if( srcIm.cols < srcIm.rows ) {
        double keep_ratio = (double)(srcIm.cols) / (double)(srcIm.rows);
        newW = (int)(FIXED_H * keep_ratio);
        newH = FIXED_H;
        resize( srcIm, dst, Size( newW, newH ) );
        int left = (FIXED_W - newW) / 2;
        int right = FIXED_W - newW - left;
        int top = 0;
        int bottom = 0;
        copyMakeBorder( dst, dst, top, bottom, left, right, BORDER_CONSTANT, Scalar(0,0,0)  );
    }
    else if( srcIm.cols > srcIm.rows ) {
        double keep_ratio = (double)(srcIm.rows) / (double)(srcIm.cols);
        newH = (int)(FIXED_W * keep_ratio);
        newW = FIXED_W;
        resize(srcIm, dst, Size( newW, newH ));
        int left = 0;
        int right = 0;
        int top = ( FIXED_H - newH ) / 2;
        int bottom = FIXED_H - newH - top;
        copyMakeBorder( dst, dst, top, bottom, left, right, BORDER_CONSTANT, Scalar(0,0,0)  );
    }
    else {
        cout<<"No need to resize and pad !"<<endl;
        return 0;
    }
    imshow("tmp", dst);
    imwrite("outimg.jpg", dst);
    waitKey();
    return 0;
}
