#include <boost/python/detail/prefix.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/default_call_policies.hpp>
#include <boost/python/object.hpp>

#include <boost/mpl/equal.hpp>

#include <algorithm>
#include <iostream>
#include <cstdio>
#include <string>
#include <cstring>

#include "opencv_converters.hpp"


// ================================================================================================

// workaround for getting a CvMat pointer
CvMat * get_CvMat_ptr(cv::Mat const &mat)
{
    if(mat.empty()) return 0;
    static int cnt = 0;
    static CvMat arr[1024];
    CvMat *result = &(arr[cnt] = mat);
    cnt = (cnt+1) & 1023;
    return result;
}


// workaround for getting an IplImage pointer
IplImage * get_IplImage_ptr(cv::Mat const &mat)
{
    if(mat.empty()) return 0;
    static int cnt = 0;
    static IplImage arr[1024];
    IplImage *result = &(arr[cnt] = mat);
    cnt = (cnt+1) & 1023;
    return result;
}

// ================================================================================================

// Mat
bool get_array_data_arrangement(cv::Mat const &inst, sdcpp::array_data_arrangement &result)
{
    if(inst.empty()) return false;
    result.item_size = inst.elemSize1();
    result.total_size = inst.rows*inst.step;
    if(inst.channels() > 1)
    {
        result.ndim = 3;
        result.size.resize(3);
        result.stride.resize(3);
        result.size[2] = inst.channels();
        result.stride[2] = inst.elemSize1();
    }
    else
    {
        result.ndim = 2;
        result.size.resize(2);
        result.stride.resize(2);
    }
    result.size[1] = inst.cols;
    result.stride[1] = inst.elemSize();
    result.size[0] = inst.rows;
    result.stride[0] = inst.step;
    return true;
}

// We don't know if MatND uses the little-endian dimension order (i.e. dim=0: lowest dimension, dim=nd-1: highest dimension) or the big-endian order. Therefore we will detect the order from the instance.
// Note: http://code.google.com/p/pyopencv/issues/detail?id=18
bool get_array_data_arrangement(cv::MatND const &inst, sdcpp::array_data_arrangement &result)
{
    if(!inst.flags) return false;

    bool endianness = (inst.dims >= 2) && (inst.step[0] > inst.step[1]);
    bool multichannel = inst.channels() > 1;
    int i;
    
    result.item_size = inst.elemSize1();
    result.ndim = inst.dims + multichannel;
    result.size.resize(result.ndim);    
    result.stride.resize(result.ndim);
    
    if(multichannel)
    {
        result.size[inst.dims] = inst.channels();
        result.stride[inst.dims] = inst.elemSize1();
    }
    
    if(endianness)
    {
        result.total_size = inst.size[0]*inst.step[0];
        for(i = 0; i < inst.dims; ++i)
        {
            result.size[i] = inst.size[i];
            result.stride[i] = inst.step[i];
        }
    }
    else
    {
        result.total_size = inst.size[inst.dims-1]*inst.step[inst.dims-1];
        for(i = 0; i < inst.dims; ++i)
        {
            result.size[i] = inst.size[inst.dims-1-i];
            result.stride[i] = inst.step[inst.dims-1-i];
        }
    }
    
    return true;
}

// IplImage
bool get_array_data_arrangement(IplImage const *inst, sdcpp::array_data_arrangement &result)
{
    return get_array_data_arrangement(cv::Mat(inst), result);
}

// CvMat
bool get_array_data_arrangement(CvMat const *inst, sdcpp::array_data_arrangement &result)
{
    return get_array_data_arrangement(cv::Mat(inst), result);
}

// CvMatND
bool get_array_data_arrangement(CvMatND const *inst, sdcpp::array_data_arrangement &result)
{
    return get_array_data_arrangement(cv::MatND(inst), result);
}

// OpenCV's MatND's shape and strides arrays are assumed big-endian
void convert_array_data_arrangement_to_opencv(const sdcpp::array_data_arrangement &arr, 
    std::vector<int> &shape, std::vector<int> &strides, int &nchannels, std::vector<bool> &contiguous)
{
    int nd = arr.ndim;
    int arr_itemsize = arr.item_size;
    if(!nd)
    {
        shape.clear();
        strides.clear();
        contiguous.clear();
        nchannels = 0; // no element at all
        return;
    }
    
    if(nd==1)
    {
        if(arr.stride[0] == arr_itemsize // is contiguous
            && 1 <= arr.size[0] && arr.size[0] <= 4) // with number of items between 1 and 4
        { // this only dimension is a multi-channel
            shape.clear();
            strides.clear();
            contiguous.clear();
            nchannels = arr.size[0];
            return;
        }

        // non-contiguous or number of items > 4
        shape.resize(1);
        shape[0] = arr.size[0];
        strides.resize(1);
        strides[0] = arr.stride[0];
        contiguous.resize(1);
        contiguous[0] = (arr.stride[0] == arr_itemsize);
        nchannels = 1;
        return;
    }
    
    // nd >= 2
    if(arr.stride[nd-1] == arr_itemsize // lowest dimension is contiguous
        && 2 <= arr.size[nd-1] && arr.size[nd-1] <= 4 // with number of items between 2 and 4
        && arr.stride[nd-2] == arr_itemsize*arr.size[nd-1]) // second lowest dimension is also contiguous
    { // then lowest dimension is a multi-channel
        nchannels = arr.size[--nd];
        arr_itemsize *= arr.size[nd];
    }
    else
        nchannels = 1;
    
    // prepare shape and strides
    int i;
    shape.resize(nd);
    strides.resize(nd);
    for(i = 0; i < nd; ++i)
    {
        shape[i] = arr.size[i];
        strides[i] = arr.stride[i];
    }
    
    // prepare contiguous
    contiguous.resize(nd);
    i = nd-1;
    contiguous[i] = (strides[i] == arr_itemsize);
    while(--i >= 0) contiguous[i] = (strides[i] == strides[i+1]*shape[i+1]);
}



// ================================================================================================

// ------------------------------------------------------------------------------------------------
// convert from a sequence of Mat to vector of Mat-equivalent type
// i.e. IplImage, CvMat, IplImage *, CvMat *, cv::Mat, cv::Mat *

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(IplImage)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = (cv::Mat const &)(bp::extract<cv::Mat const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(IplImage *)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = get_IplImage_ptr(bp::extract<cv::Mat const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(CvMat)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = (cv::Mat const &)(bp::extract<cv::Mat const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(CvMat *)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = get_CvMat_ptr(bp::extract<cv::Mat const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(cv::Mat)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = bp::extract<cv::Mat &>(in_arr[i]);
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(cv::Mat *)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = bp::extract<cv::Mat *>(in_arr[i]);
}

CONVERT_FROM_SEQ_OF_MAT_TO_VECTOR_OF_T(cv::Ptr<cv::Mat>)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i)
    {
        cv::Mat *obj = new cv::Mat();
        *obj = bp::extract<cv::Mat const &>(in_arr[i]);
        out_arr[i] = cv::Ptr<cv::Mat>(obj);
    }
}



// ================================================================================================

// workaround for getting a CvMatND pointer
CvMatND * get_CvMatND_ptr(cv::MatND const &matnd)
{
    if(!matnd.data) return 0;
    static int cnt = 0;
    static CvMatND arr[1024];
    CvMatND *result = &(arr[cnt] = matnd);
    cnt = (cnt+1) & 1023;
    return result;
}


// convert from a sequence of MatND to vector of MatND-equivalent type
// i.e. CvMatND, CvMatND *, cv::MatND, cv::MatND *
CONVERT_FROM_SEQ_OF_MATND_TO_VECTOR_OF_T(CvMatND)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = (cv::MatND const &)(bp::extract<cv::MatND const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MATND_TO_VECTOR_OF_T(CvMatND *)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = get_CvMatND_ptr(bp::extract<cv::MatND const &>(in_arr[i]));
}

CONVERT_FROM_SEQ_OF_MATND_TO_VECTOR_OF_T(cv::MatND)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = bp::extract<cv::MatND &>(in_arr[i]);
}

CONVERT_FROM_SEQ_OF_MATND_TO_VECTOR_OF_T(cv::MatND *)
{
    bp::object const &in_arr = in_seq.get_obj();
    int len = bp::len(in_arr);
    out_arr.resize(len);
    for(int i = 0; i < len; ++i) 
        out_arr[i] = bp::extract<cv::MatND *>(in_arr[i]);
}




// ================================================================================================

// convert_vector_to_seq

#define CONVERT_VECTOR_TO_NDARRAY(VectType) \
CONVERT_VECTOR_TO_SEQ(VectType) \
{ \
    sdcpp::ndarray out_arr = sdcpp::simplenew_ndarray(0,0,5); \
    sdcpp::vector_to_ndarray(in_arr, out_arr); \
    return sdcpp::sequence(out_arr.get_obj()); \
}

// basic
CONVERT_VECTOR_TO_NDARRAY(char);
CONVERT_VECTOR_TO_NDARRAY(unsigned char);
CONVERT_VECTOR_TO_NDARRAY(short);
CONVERT_VECTOR_TO_NDARRAY(unsigned short);
CONVERT_VECTOR_TO_NDARRAY(long);
CONVERT_VECTOR_TO_NDARRAY(unsigned long);
CONVERT_VECTOR_TO_NDARRAY(int);
CONVERT_VECTOR_TO_NDARRAY(unsigned int);
CONVERT_VECTOR_TO_NDARRAY(float);
CONVERT_VECTOR_TO_NDARRAY(double);

// Vec-like
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2b);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3b);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4b);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2s);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3s);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4s);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2w);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3w);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4w);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2i);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3i);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4i);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2f);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3f);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4f);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec6f);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec2d);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec3d);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec4d);
CONVERT_VECTOR_TO_NDARRAY(cv::Vec6d);

// Point-like
CONVERT_VECTOR_TO_NDARRAY(cv::Point2i);
CONVERT_VECTOR_TO_NDARRAY(cv::Point2f);
CONVERT_VECTOR_TO_NDARRAY(cv::Point2d);
CONVERT_VECTOR_TO_NDARRAY(cv::Point3i);
CONVERT_VECTOR_TO_NDARRAY(cv::Point3f);
CONVERT_VECTOR_TO_NDARRAY(cv::Point3d);

// Rect-like
CONVERT_VECTOR_TO_NDARRAY(cv::Rect);
CONVERT_VECTOR_TO_NDARRAY(cv::Rectf);
CONVERT_VECTOR_TO_NDARRAY(cv::Rectd);
CONVERT_VECTOR_TO_NDARRAY(cv::RotatedRect);

// Size-like
CONVERT_VECTOR_TO_NDARRAY(cv::Size2i);
CONVERT_VECTOR_TO_NDARRAY(cv::Size2f);
CONVERT_VECTOR_TO_NDARRAY(cv::Size2d);

// Scalar
CONVERT_VECTOR_TO_NDARRAY(cv::Scalar);

// Range
CONVERT_VECTOR_TO_NDARRAY(cv::Range);



// ================================================================================================

namespace mpl=boost::mpl;

template<typename T>
struct sdconverter;

template<typename T>
struct sdconverter_simple
{
    typedef T pytype;
    void from_python(bp::object const &py_obj, T &cpp_obj) { cpp_obj = bp::extract<T>(py_obj); }
    void to_python(T const &cpp_obj, bp::object &py_obj)
    {
        T &py_obj2 = bp::extract<T &>(py_obj);
        py_obj2 = cpp_obj;
    }
    T new_pyobj() { return T(); }
};

template<>
struct sdconverter_simple< cv::Ptr<cv::Mat> >
{
    typedef cv::Mat pytype;
    void from_python(bp::object const &py_obj, cv::Ptr<cv::Mat> &cpp_obj)
    {
        cv::Mat *py_obj2 = new cv::Mat();
        *py_obj2 = bp::extract<cv::Mat const &>(py_obj);
        cpp_obj = cv::Ptr<cv::Mat>(py_obj2);
    }
    void to_python(cv::Ptr<cv::Mat> const &cpp_obj, bp::object &py_obj)
    {
        pytype &py_obj2 = bp::extract<pytype &>(py_obj);
        py_obj2 = *cpp_obj;
    }
    cv::Ptr<cv::Mat> new_pyobj() { return cv::Ptr<cv::Mat>(new cv::Mat()); }
};

template<typename T>
struct sdconverter_vector
{
    typedef bp::list pytype;
    void from_python(bp::object const &py_obj, std::vector<T> &cpp_obj)
    {
        int n = bp::len(py_obj);
        cpp_obj.resize(n);
        for(int i = 0; i < n; ++i)
            sdconverter<T>::impl_t::from_python(py_obj[i], cpp_obj[i]);
    }
    void to_python(std::vector<T> const &cpp_obj, bp::object &py_obj)
    {
        int n = cpp_obj.size(), n2 = bp::len(py_obj);
        bp::extract<bp::list> py_obj2(py_obj);
        while(n2 > n) { py_obj2().pop(); --n2; }
        if(!n) return;
        bp::object obj;
        for(int i = 0; i < n; ++i)
        {
            if(i == n2)
            {
                py_obj2().append(bp::object(sdconverter<T>::impl_t::new_pyobj()));
                ++n2;
            }
            else if(!bp::extract<typename sdconverter<T>::impl_t::pytype>(py_obj[i]).check())
                py_obj[i] = bp::object(sdconverter<T>::impl_t::new_pyobj());
                
            obj = py_obj[i];
            sdconverter<T>::impl_t::to_python(cpp_obj[i], obj);
            py_obj[i] = obj;
        }
    }
    bp::list new_pyobj() { return bp::list(); }
};

template<typename T>
struct sdconverter
{
    typedef typename mpl::if_<
        mpl::equal< std::vector<typename mpl::deref<typename mpl::begin<T>::type >::type >, T >,
        sdconverter_vector<typename mpl::deref<typename mpl::begin<T>::type >::type >,
        sdconverter_simple<T>
    >::type impl_t;
};