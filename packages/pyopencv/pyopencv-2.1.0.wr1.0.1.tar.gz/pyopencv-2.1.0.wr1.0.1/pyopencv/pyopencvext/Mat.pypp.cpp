// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "opencv_converters.hpp"
#include "ndarray.hpp"
#include "Mat.pypp.hpp"

namespace bp = boost::python;

static bp::object get_data(cv::Mat const &inst)
{
    return bp::object(bp::handle<>(PyBuffer_FromReadWriteMemory ((void*)inst.data, inst.rows*inst.step)));
}

static boost::shared_ptr<cv::Mat> Mat__init1__(bp::object const &arg1)
{
    // None
    if(arg1.ptr() == Py_None) return boost::shared_ptr<cv::Mat>(new cv::Mat());
    
    // cv::Mat const &
    bp::extract<cv::Mat const &> arg1a(arg1);
    if(arg1a.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1a()));
    
    // TODO: here
    PyErr_SetString(PyExc_NotImplementedError, "Unable to construct cv::Mat using the given argument.");
    throw bp::error_already_set(); 
    return boost::shared_ptr<cv::Mat>(new cv::Mat());
}

static boost::shared_ptr<cv::Mat> Mat__init2__(bp::object const &arg1, bp::object const &arg2)
{
    // cv::Size, int
    bp::extract<cv::Size const &> arg1a(arg1);
    bp::extract<int> arg2a(arg2);
    if(arg1a.check() && arg2a.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1a(), arg2a()));
    
    // cv::Mat, cv::Rect
    bp::extract<cv::Mat const &> arg1b(arg1);
    bp::extract<cv::Rect> arg2b(arg2);
    if(arg1b.check() && arg2b.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1b(), arg2b()));
    
    // TODO: here
    PyErr_SetString(PyExc_NotImplementedError, "Unable to construct cv::Mat using the given 2 arguments.");
    throw bp::error_already_set(); 
    return boost::shared_ptr<cv::Mat>(new cv::Mat());
}

static boost::shared_ptr<cv::Mat> Mat__init3__(bp::object const &arg1, bp::object const &arg2, bp::object const &arg3)
{
    // int, int, int
    bp::extract<int> arg1a(arg1);
    bp::extract<int> arg2a(arg2);
    bp::extract<int> arg3a(arg3);
    if(arg1a.check() && arg2a.check() && arg3a.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1a(), arg2a(), arg3a()));
    
    // cv::Size, int, cv::Scalar
    bp::extract<cv::Size const &> arg1b(arg1);
    bp::extract<int> arg2b(arg2);
    bp::extract<cv::Scalar const &> arg3b(arg3);
    if(arg1b.check() && arg2b.check() && arg3b.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1b(), arg2b(), arg3b()));
    
    // cv::Mat, cv::Range, cv::Range
    bp::extract<cv::Mat const &> arg1c(arg1);
    bp::extract<cv::Range const &> arg2c(arg2);
    bp::extract<cv::Range const &> arg3c(arg3);
    if(arg1c.check() && arg2c.check() && arg3c.check()) return boost::shared_ptr<cv::Mat>(new cv::Mat(arg1c(), arg2c(), arg3c()));
    
    // TODO: here
    PyErr_SetString(PyExc_NotImplementedError, "Unable to construct cv::Mat using the given 3 arguments.");
    throw bp::error_already_set(); 
    return boost::shared_ptr<cv::Mat>(new cv::Mat());
}

void register_Mat_class(){

    { //::cv::Mat
        typedef bp::class_< cv::Mat > Mat_exposer_t;
        Mat_exposer_t Mat_exposer = Mat_exposer_t( "Mat", bp::init< >() );
        bp::scope Mat_scope( Mat_exposer );
        Mat_exposer.add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::Mat >() );
        bp::scope().attr("MAGIC_VAL") = (int)cv::Mat::MAGIC_VAL;
        bp::scope().attr("AUTO_STEP") = (int)cv::Mat::AUTO_STEP;
        bp::scope().attr("CONTINUOUS_FLAG") = (int)cv::Mat::CONTINUOUS_FLAG;
        Mat_exposer.def( bp::init< int, int, int >(( bp::arg("_rows"), bp::arg("_cols"), bp::arg("_type") )) );
        Mat_exposer.def( bp::init< int, int, int, cv::Scalar const & >(( bp::arg("_rows"), bp::arg("_cols"), bp::arg("_type"), bp::arg("_s") )) );
        Mat_exposer.def( bp::init< cv::Size, int >(( bp::arg("_size"), bp::arg("_type") )) );
        Mat_exposer.def( bp::init< cv::Size, int, cv::Scalar const & >(( bp::arg("_size"), bp::arg("_type"), bp::arg("_s") )) );
        Mat_exposer.def( bp::init< cv::Mat const & >(( bp::arg("m") )) );
        Mat_exposer.def( bp::init< cv::Mat const &, cv::Range const &, cv::Range const & >(( bp::arg("m"), bp::arg("rowRange"), bp::arg("colRange") )) );
        Mat_exposer.def( bp::init< cv::Mat const &, cv::Rect const & >(( bp::arg("m"), bp::arg("roi") )) );
        { //::cv::Mat::addref
        
            typedef void ( ::cv::Mat::*addref_function_type )(  ) ;
            
            Mat_exposer.def( 
                "addref"
                , addref_function_type( &::cv::Mat::addref ) );
        
        }
        { //::cv::Mat::adjustROI
        
            typedef ::cv::Mat & ( ::cv::Mat::*adjustROI_function_type )( int,int,int,int ) ;
            
            Mat_exposer.def( 
                "adjustROI"
                , adjustROI_function_type( &::cv::Mat::adjustROI )
                , ( bp::arg("dtop"), bp::arg("dbottom"), bp::arg("dleft"), bp::arg("dright") )
                , bp::return_self< >() );
        
        }
        { //::cv::Mat::assignTo
        
            typedef void ( ::cv::Mat::*assignTo_function_type )( ::cv::Mat &,int ) const;
            
            Mat_exposer.def( 
                "assignTo"
                , assignTo_function_type( &::cv::Mat::assignTo )
                , ( bp::arg("m"), bp::arg("type")=(int)(-0x000000001) ) );
        
        }
        { //::cv::Mat::channels
        
            typedef int ( ::cv::Mat::*channels_function_type )(  ) const;
            
            Mat_exposer.def( 
                "channels"
                , channels_function_type( &::cv::Mat::channels ) );
        
        }
        { //::cv::Mat::clone
        
            typedef ::cv::Mat ( ::cv::Mat::*clone_function_type )(  ) const;
            
            Mat_exposer.def( 
                "clone"
                , clone_function_type( &::cv::Mat::clone ) );
        
        }
        { //::cv::Mat::col
        
            typedef ::cv::Mat ( ::cv::Mat::*col_function_type )( int ) const;
            
            Mat_exposer.def( 
                "col"
                , col_function_type( &::cv::Mat::col )
                , ( bp::arg("x") ) );
        
        }
        { //::cv::Mat::colRange
        
            typedef ::cv::Mat ( ::cv::Mat::*colRange_function_type )( int,int ) const;
            
            Mat_exposer.def( 
                "colRange"
                , colRange_function_type( &::cv::Mat::colRange )
                , ( bp::arg("startcol"), bp::arg("endcol") ) );
        
        }
        { //::cv::Mat::colRange
        
            typedef ::cv::Mat ( ::cv::Mat::*colRange_function_type )( ::cv::Range const & ) const;
            
            Mat_exposer.def( 
                "colRange"
                , colRange_function_type( &::cv::Mat::colRange )
                , ( bp::arg("r") ) );
        
        }
        { //::cv::Mat::convertTo
        
            typedef void ( ::cv::Mat::*convertTo_function_type )( ::cv::Mat &,int,double,double ) const;
            
            Mat_exposer.def( 
                "convertTo"
                , convertTo_function_type( &::cv::Mat::convertTo )
                , ( bp::arg("m"), bp::arg("rtype"), bp::arg("alpha")=1, bp::arg("beta")=0 ) );
        
        }
        { //::cv::Mat::copyTo
        
            typedef void ( ::cv::Mat::*copyTo_function_type )( ::cv::Mat & ) const;
            
            Mat_exposer.def( 
                "copyTo"
                , copyTo_function_type( &::cv::Mat::copyTo )
                , ( bp::arg("m") ) );
        
        }
        { //::cv::Mat::copyTo
        
            typedef void ( ::cv::Mat::*copyTo_function_type )( ::cv::Mat &,::cv::Mat const & ) const;
            
            Mat_exposer.def( 
                "copyTo"
                , copyTo_function_type( &::cv::Mat::copyTo )
                , ( bp::arg("m"), bp::arg("mask") ) );
        
        }
        { //::cv::Mat::create
        
            typedef void ( ::cv::Mat::*create_function_type )( int,int,int ) ;
            
            Mat_exposer.def( 
                "create"
                , create_function_type( &::cv::Mat::create )
                , ( bp::arg("_rows"), bp::arg("_cols"), bp::arg("_type") ) );
        
        }
        { //::cv::Mat::create
        
            typedef void ( ::cv::Mat::*create_function_type )( ::cv::Size,int ) ;
            
            Mat_exposer.def( 
                "create"
                , create_function_type( &::cv::Mat::create )
                , ( bp::arg("_size"), bp::arg("_type") ) );
        
        }
        { //::cv::Mat::cross
        
            typedef ::cv::Mat ( ::cv::Mat::*cross_function_type )( ::cv::Mat const & ) const;
            
            Mat_exposer.def( 
                "cross"
                , cross_function_type( &::cv::Mat::cross )
                , ( bp::arg("m") ) );
        
        }
        { //::cv::Mat::depth
        
            typedef int ( ::cv::Mat::*depth_function_type )(  ) const;
            
            Mat_exposer.def( 
                "depth"
                , depth_function_type( &::cv::Mat::depth ) );
        
        }
        { //::cv::Mat::diag
        
            typedef ::cv::Mat ( ::cv::Mat::*diag_function_type )( int ) const;
            
            Mat_exposer.def( 
                "diag"
                , diag_function_type( &::cv::Mat::diag )
                , ( bp::arg("d")=(int)(0) ) );
        
        }
        { //::cv::Mat::diag
        
            typedef ::cv::Mat ( *diag_function_type )( ::cv::Mat const & );
            
            Mat_exposer.def( 
                "diag"
                , diag_function_type( &::cv::Mat::diag )
                , ( bp::arg("d") ) );
        
        }
        { //::cv::Mat::dot
        
            typedef double ( ::cv::Mat::*dot_function_type )( ::cv::Mat const & ) const;
            
            Mat_exposer.def( 
                "dot"
                , dot_function_type( &::cv::Mat::dot )
                , ( bp::arg("m") ) );
        
        }
        { //::cv::Mat::elemSize
        
            typedef ::size_t ( ::cv::Mat::*elemSize_function_type )(  ) const;
            
            Mat_exposer.def( 
                "elemSize"
                , elemSize_function_type( &::cv::Mat::elemSize ) );
        
        }
        { //::cv::Mat::elemSize1
        
            typedef ::size_t ( ::cv::Mat::*elemSize1_function_type )(  ) const;
            
            Mat_exposer.def( 
                "elemSize1"
                , elemSize1_function_type( &::cv::Mat::elemSize1 ) );
        
        }
        { //::cv::Mat::empty
        
            typedef bool ( ::cv::Mat::*empty_function_type )(  ) const;
            
            Mat_exposer.def( 
                "empty"
                , empty_function_type( &::cv::Mat::empty ) );
        
        }
        { //::cv::Mat::isContinuous
        
            typedef bool ( ::cv::Mat::*isContinuous_function_type )(  ) const;
            
            Mat_exposer.def( 
                "isContinuous"
                , isContinuous_function_type( &::cv::Mat::isContinuous ) );
        
        }
        { //::cv::Mat::locateROI
        
            typedef void ( ::cv::Mat::*locateROI_function_type )( ::cv::Size &,::cv::Point & ) const;
            
            Mat_exposer.def( 
                "locateROI"
                , locateROI_function_type( &::cv::Mat::locateROI )
                , ( bp::arg("wholeSize"), bp::arg("ofs") ) );
        
        }
        { //::cv::Mat::operator()
        
            typedef ::cv::Mat ( ::cv::Mat::*__call___function_type )( ::cv::Range,::cv::Range ) const;
            
            Mat_exposer.def( 
                "__call__"
                , __call___function_type( &::cv::Mat::operator() )
                , ( bp::arg("rowRange"), bp::arg("colRange") ) );
        
        }
        { //::cv::Mat::operator()
        
            typedef ::cv::Mat ( ::cv::Mat::*__call___function_type )( ::cv::Rect const & ) const;
            
            Mat_exposer.def( 
                "__call__"
                , __call___function_type( &::cv::Mat::operator() )
                , ( bp::arg("roi") ) );
        
        }
        { //::cv::Mat::operator=
        
            typedef ::cv::Mat & ( ::cv::Mat::*assign_function_type )( ::cv::Mat const & ) ;
            
            Mat_exposer.def( 
                "assign"
                , assign_function_type( &::cv::Mat::operator= )
                , ( bp::arg("m") )
                , bp::return_self< >() );
        
        }
        { //::cv::Mat::operator=
        
            typedef ::cv::Mat & ( ::cv::Mat::*assign_function_type )( ::cv::Scalar const & ) ;
            
            Mat_exposer.def( 
                "assign"
                , assign_function_type( &::cv::Mat::operator= )
                , ( bp::arg("s") )
                , bp::return_self< >() );
        
        }
        { //::cv::Mat::release
        
            typedef void ( ::cv::Mat::*release_function_type )(  ) ;
            
            Mat_exposer.def( 
                "release"
                , release_function_type( &::cv::Mat::release ) );
        
        }
        { //::cv::Mat::reshape
        
            typedef ::cv::Mat ( ::cv::Mat::*reshape_function_type )( int,int ) const;
            
            Mat_exposer.def( 
                "reshape"
                , reshape_function_type( &::cv::Mat::reshape )
                , ( bp::arg("_cn"), bp::arg("_rows")=(int)(0) ) );
        
        }
        { //::cv::Mat::row
        
            typedef ::cv::Mat ( ::cv::Mat::*row_function_type )( int ) const;
            
            Mat_exposer.def( 
                "row"
                , row_function_type( &::cv::Mat::row )
                , ( bp::arg("y") ) );
        
        }
        { //::cv::Mat::rowRange
        
            typedef ::cv::Mat ( ::cv::Mat::*rowRange_function_type )( int,int ) const;
            
            Mat_exposer.def( 
                "rowRange"
                , rowRange_function_type( &::cv::Mat::rowRange )
                , ( bp::arg("startrow"), bp::arg("endrow") ) );
        
        }
        { //::cv::Mat::rowRange
        
            typedef ::cv::Mat ( ::cv::Mat::*rowRange_function_type )( ::cv::Range const & ) const;
            
            Mat_exposer.def( 
                "rowRange"
                , rowRange_function_type( &::cv::Mat::rowRange )
                , ( bp::arg("r") ) );
        
        }
        { //::cv::Mat::setTo
        
            typedef ::cv::Mat & ( ::cv::Mat::*setTo_function_type )( ::cv::Scalar const &,::cv::Mat const & ) ;
            
            Mat_exposer.def( 
                "setTo"
                , setTo_function_type( &::cv::Mat::setTo )
                , ( bp::arg("s"), bp::arg("mask")=cv::Mat() )
                , bp::return_self< >() );
        
        }
        { //::cv::Mat::size
        
            typedef ::cv::Size ( ::cv::Mat::*size_function_type )(  ) const;
            
            Mat_exposer.def( 
                "size"
                , size_function_type( &::cv::Mat::size ) );
        
        }
        { //::cv::Mat::step1
        
            typedef ::size_t ( ::cv::Mat::*step1_function_type )(  ) const;
            
            Mat_exposer.def( 
                "step1"
                , step1_function_type( &::cv::Mat::step1 ) );
        
        }
        { //::cv::Mat::type
        
            typedef int ( ::cv::Mat::*type_function_type )(  ) const;
            
            Mat_exposer.def( 
                "type"
                , type_function_type( &::cv::Mat::type ) );
        
        }
        Mat_exposer.def_readwrite( "cols", &cv::Mat::cols );
        Mat_exposer.def_readwrite( "flags", &cv::Mat::flags );
        Mat_exposer.def_readwrite( "rows", &cv::Mat::rows );
        Mat_exposer.def_readwrite( "step", &cv::Mat::step );
        Mat_exposer.staticmethod( "diag" );
        Mat_exposer.add_property("data", &::get_data);
        Mat_exposer.def("from_ndarray", &bp::from_ndarray< cv::Mat >, (bp::arg("arr")) );
        Mat_exposer.staticmethod("from_ndarray");
        Mat_exposer.add_property("ndarray", &bp::as_ndarray< cv::Mat >);
        Mat_exposer.def("__init__", bp::make_constructor(&Mat__init1__, bp::default_call_policies(), ( bp::arg("arg1") )));
        Mat_exposer.def("__init__", bp::make_constructor(&Mat__init2__, bp::default_call_policies(), ( bp::arg("arg1"), bp::arg("arg2") )));
        Mat_exposer.def("__init__", bp::make_constructor(&Mat__init3__, bp::default_call_policies(), ( bp::arg("arg1"), bp::arg("arg2"), bp::arg("arg3") )));
        Mat_exposer.def("to_list_of_int32", &convert_from_Mat_to_seq<int> );
        Mat_exposer.def("from_list_of_int32", &convert_from_seq_to_Mat_object<int> );
        Mat_exposer.staticmethod("from_list_of_int32");
        Mat_exposer.def("to_list_of_int16", &convert_from_Mat_to_seq<short> );
        Mat_exposer.def("from_list_of_int16", &convert_from_seq_to_Mat_object<short> );
        Mat_exposer.staticmethod("from_list_of_int16");
        Mat_exposer.def("to_list_of_Vec4b", &convert_from_Mat_to_seq<cv::Vec4b> );
        Mat_exposer.def("from_list_of_Vec4b", &convert_from_seq_to_Mat_object<cv::Vec4b> );
        Mat_exposer.staticmethod("from_list_of_Vec4b");
        Mat_exposer.def("to_list_of_Vec4f", &convert_from_Mat_to_seq<cv::Vec4f> );
        Mat_exposer.def("from_list_of_Vec4f", &convert_from_seq_to_Mat_object<cv::Vec4f> );
        Mat_exposer.staticmethod("from_list_of_Vec4f");
        Mat_exposer.def("to_list_of_uint8", &convert_from_Mat_to_seq<unsigned char> );
        Mat_exposer.def("from_list_of_uint8", &convert_from_seq_to_Mat_object<unsigned char> );
        Mat_exposer.staticmethod("from_list_of_uint8");
        Mat_exposer.def("to_list_of_Vec4i", &convert_from_Mat_to_seq<cv::Vec4i> );
        Mat_exposer.def("from_list_of_Vec4i", &convert_from_seq_to_Mat_object<cv::Vec4i> );
        Mat_exposer.staticmethod("from_list_of_Vec4i");
        Mat_exposer.def("to_list_of_Rectf", &convert_from_Mat_to_seq<cv::Rectf> );
        Mat_exposer.def("from_list_of_Rectf", &convert_from_seq_to_Mat_object<cv::Rectf> );
        Mat_exposer.staticmethod("from_list_of_Rectf");
        Mat_exposer.def("to_list_of_Vec4w", &convert_from_Mat_to_seq<cv::Vec4w> );
        Mat_exposer.def("from_list_of_Vec4w", &convert_from_seq_to_Mat_object<cv::Vec4w> );
        Mat_exposer.staticmethod("from_list_of_Vec4w");
        Mat_exposer.def("to_list_of_Point3i", &convert_from_Mat_to_seq<cv::Point3i> );
        Mat_exposer.def("from_list_of_Point3i", &convert_from_seq_to_Mat_object<cv::Point3i> );
        Mat_exposer.staticmethod("from_list_of_Point3i");
        Mat_exposer.def("to_list_of_Point2i", &convert_from_Mat_to_seq<cv::Point2i> );
        Mat_exposer.def("from_list_of_Point2i", &convert_from_seq_to_Mat_object<cv::Point2i> );
        Mat_exposer.staticmethod("from_list_of_Point2i");
        Mat_exposer.def("to_list_of_Vec4d", &convert_from_Mat_to_seq<cv::Vec4d> );
        Mat_exposer.def("from_list_of_Vec4d", &convert_from_seq_to_Mat_object<cv::Vec4d> );
        Mat_exposer.staticmethod("from_list_of_Vec4d");
        Mat_exposer.def("to_list_of_Vec4s", &convert_from_Mat_to_seq<cv::Vec4s> );
        Mat_exposer.def("from_list_of_Vec4s", &convert_from_seq_to_Mat_object<cv::Vec4s> );
        Mat_exposer.staticmethod("from_list_of_Vec4s");
        Mat_exposer.def("to_list_of_Vec2f", &convert_from_Mat_to_seq<cv::Vec2f> );
        Mat_exposer.def("from_list_of_Vec2f", &convert_from_seq_to_Mat_object<cv::Vec2f> );
        Mat_exposer.staticmethod("from_list_of_Vec2f");
        Mat_exposer.def("to_list_of_Range", &convert_from_Mat_to_seq<cv::Range> );
        Mat_exposer.def("from_list_of_Range", &convert_from_seq_to_Mat_object<cv::Range> );
        Mat_exposer.staticmethod("from_list_of_Range");
        Mat_exposer.def("to_list_of_RotatedRect", &convert_from_Mat_to_seq<cv::RotatedRect> );
        Mat_exposer.def("from_list_of_RotatedRect", &convert_from_seq_to_Mat_object<cv::RotatedRect> );
        Mat_exposer.staticmethod("from_list_of_RotatedRect");
        Mat_exposer.def("to_list_of_Rectd", &convert_from_Mat_to_seq<cv::Rectd> );
        Mat_exposer.def("from_list_of_Rectd", &convert_from_seq_to_Mat_object<cv::Rectd> );
        Mat_exposer.staticmethod("from_list_of_Rectd");
        Mat_exposer.def("to_list_of_Point3d", &convert_from_Mat_to_seq<cv::Point3d> );
        Mat_exposer.def("from_list_of_Point3d", &convert_from_seq_to_Mat_object<cv::Point3d> );
        Mat_exposer.staticmethod("from_list_of_Point3d");
        Mat_exposer.def("to_list_of_int8", &convert_from_Mat_to_seq<char> );
        Mat_exposer.def("from_list_of_int8", &convert_from_seq_to_Mat_object<char> );
        Mat_exposer.staticmethod("from_list_of_int8");
        Mat_exposer.def("to_list_of_Point3f", &convert_from_Mat_to_seq<cv::Point3f> );
        Mat_exposer.def("from_list_of_Point3f", &convert_from_seq_to_Mat_object<cv::Point3f> );
        Mat_exposer.staticmethod("from_list_of_Point3f");
        Mat_exposer.def("to_list_of_Point2d", &convert_from_Mat_to_seq<cv::Point2d> );
        Mat_exposer.def("from_list_of_Point2d", &convert_from_seq_to_Mat_object<cv::Point2d> );
        Mat_exposer.staticmethod("from_list_of_Point2d");
        Mat_exposer.def("to_list_of_Vec3w", &convert_from_Mat_to_seq<cv::Vec3w> );
        Mat_exposer.def("from_list_of_Vec3w", &convert_from_seq_to_Mat_object<cv::Vec3w> );
        Mat_exposer.staticmethod("from_list_of_Vec3w");
        Mat_exposer.def("to_list_of_Vec2w", &convert_from_Mat_to_seq<cv::Vec2w> );
        Mat_exposer.def("from_list_of_Vec2w", &convert_from_seq_to_Mat_object<cv::Vec2w> );
        Mat_exposer.staticmethod("from_list_of_Vec2w");
        Mat_exposer.def("to_list_of_Vec3s", &convert_from_Mat_to_seq<cv::Vec3s> );
        Mat_exposer.def("from_list_of_Vec3s", &convert_from_seq_to_Mat_object<cv::Vec3s> );
        Mat_exposer.staticmethod("from_list_of_Vec3s");
        Mat_exposer.def("to_list_of_Vec2s", &convert_from_Mat_to_seq<cv::Vec2s> );
        Mat_exposer.def("from_list_of_Vec2s", &convert_from_seq_to_Mat_object<cv::Vec2s> );
        Mat_exposer.staticmethod("from_list_of_Vec2s");
        Mat_exposer.def("to_list_of_float64", &convert_from_Mat_to_seq<double> );
        Mat_exposer.def("from_list_of_float64", &convert_from_seq_to_Mat_object<double> );
        Mat_exposer.staticmethod("from_list_of_float64");
        Mat_exposer.def("to_list_of_Size2f", &convert_from_Mat_to_seq<cv::Size2f> );
        Mat_exposer.def("from_list_of_Size2f", &convert_from_seq_to_Mat_object<cv::Size2f> );
        Mat_exposer.staticmethod("from_list_of_Size2f");
        Mat_exposer.def("to_list_of_Size2i", &convert_from_Mat_to_seq<cv::Size2i> );
        Mat_exposer.def("from_list_of_Size2i", &convert_from_seq_to_Mat_object<cv::Size2i> );
        Mat_exposer.staticmethod("from_list_of_Size2i");
        Mat_exposer.def("to_list_of_Size2d", &convert_from_Mat_to_seq<cv::Size2d> );
        Mat_exposer.def("from_list_of_Size2d", &convert_from_seq_to_Mat_object<cv::Size2d> );
        Mat_exposer.staticmethod("from_list_of_Size2d");
        Mat_exposer.def("to_list_of_Scalar", &convert_from_Mat_to_seq<cv::Scalar> );
        Mat_exposer.def("from_list_of_Scalar", &convert_from_seq_to_Mat_object<cv::Scalar> );
        Mat_exposer.staticmethod("from_list_of_Scalar");
        Mat_exposer.def("to_list_of_Point2f", &convert_from_Mat_to_seq<cv::Point2f> );
        Mat_exposer.def("from_list_of_Point2f", &convert_from_seq_to_Mat_object<cv::Point2f> );
        Mat_exposer.staticmethod("from_list_of_Point2f");
        Mat_exposer.def("to_list_of_Vec3f", &convert_from_Mat_to_seq<cv::Vec3f> );
        Mat_exposer.def("from_list_of_Vec3f", &convert_from_seq_to_Mat_object<cv::Vec3f> );
        Mat_exposer.staticmethod("from_list_of_Vec3f");
        Mat_exposer.def("to_list_of_Vec2d", &convert_from_Mat_to_seq<cv::Vec2d> );
        Mat_exposer.def("from_list_of_Vec2d", &convert_from_seq_to_Mat_object<cv::Vec2d> );
        Mat_exposer.staticmethod("from_list_of_Vec2d");
        Mat_exposer.def("to_list_of_Vec3d", &convert_from_Mat_to_seq<cv::Vec3d> );
        Mat_exposer.def("from_list_of_Vec3d", &convert_from_seq_to_Mat_object<cv::Vec3d> );
        Mat_exposer.staticmethod("from_list_of_Vec3d");
        Mat_exposer.def("to_list_of_uint16", &convert_from_Mat_to_seq<unsigned short> );
        Mat_exposer.def("from_list_of_uint16", &convert_from_seq_to_Mat_object<unsigned short> );
        Mat_exposer.staticmethod("from_list_of_uint16");
        Mat_exposer.def("to_list_of_Vec3b", &convert_from_Mat_to_seq<cv::Vec3b> );
        Mat_exposer.def("from_list_of_Vec3b", &convert_from_seq_to_Mat_object<cv::Vec3b> );
        Mat_exposer.staticmethod("from_list_of_Vec3b");
        Mat_exposer.def("to_list_of_Rect", &convert_from_Mat_to_seq<cv::Rect> );
        Mat_exposer.def("from_list_of_Rect", &convert_from_seq_to_Mat_object<cv::Rect> );
        Mat_exposer.staticmethod("from_list_of_Rect");
        Mat_exposer.def("to_list_of_Vec2b", &convert_from_Mat_to_seq<cv::Vec2b> );
        Mat_exposer.def("from_list_of_Vec2b", &convert_from_seq_to_Mat_object<cv::Vec2b> );
        Mat_exposer.staticmethod("from_list_of_Vec2b");
        Mat_exposer.def("to_list_of_Vec6f", &convert_from_Mat_to_seq<cv::Vec6f> );
        Mat_exposer.def("from_list_of_Vec6f", &convert_from_seq_to_Mat_object<cv::Vec6f> );
        Mat_exposer.staticmethod("from_list_of_Vec6f");
        Mat_exposer.def("to_list_of_Vec2i", &convert_from_Mat_to_seq<cv::Vec2i> );
        Mat_exposer.def("from_list_of_Vec2i", &convert_from_seq_to_Mat_object<cv::Vec2i> );
        Mat_exposer.staticmethod("from_list_of_Vec2i");
        Mat_exposer.def("to_list_of_Vec6d", &convert_from_Mat_to_seq<cv::Vec6d> );
        Mat_exposer.def("from_list_of_Vec6d", &convert_from_seq_to_Mat_object<cv::Vec6d> );
        Mat_exposer.staticmethod("from_list_of_Vec6d");
        Mat_exposer.def("to_list_of_float32", &convert_from_Mat_to_seq<float> );
        Mat_exposer.def("from_list_of_float32", &convert_from_seq_to_Mat_object<float> );
        Mat_exposer.staticmethod("from_list_of_float32");
        Mat_exposer.def("to_list_of_Vec3i", &convert_from_Mat_to_seq<cv::Vec3i> );
        Mat_exposer.def("from_list_of_Vec3i", &convert_from_seq_to_Mat_object<cv::Vec3i> );
        Mat_exposer.staticmethod("from_list_of_Vec3i");
    }

}
