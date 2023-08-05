// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "BackgroundSubtractor.pypp.hpp"

namespace bp = boost::python;

struct BackgroundSubtractor_wrapper : cv::BackgroundSubtractor, bp::wrapper< cv::BackgroundSubtractor > {

    BackgroundSubtractor_wrapper(cv::BackgroundSubtractor const & arg )
    : cv::BackgroundSubtractor( arg )
      , bp::wrapper< cv::BackgroundSubtractor >(){
        // copy constructor
        
    }

    BackgroundSubtractor_wrapper()
    : cv::BackgroundSubtractor()
      , bp::wrapper< cv::BackgroundSubtractor >(){
        // null constructor
        
    }

    virtual void operator()( ::cv::Mat const & image, ::cv::Mat & fgmask, double learningRate=0 ) {
        if( bp::override func___call__ = this->get_override( "__call__" ) )
            func___call__( boost::ref(image), boost::ref(fgmask), learningRate );
        else{
            this->cv::BackgroundSubtractor::operator()( boost::ref(image), boost::ref(fgmask), learningRate );
        }
    }
    
    void default___call__( ::cv::Mat const & image, ::cv::Mat & fgmask, double learningRate=0 ) {
        cv::BackgroundSubtractor::operator()( boost::ref(image), boost::ref(fgmask), learningRate );
    }

};

void register_BackgroundSubtractor_class(){

    bp::class_< BackgroundSubtractor_wrapper >( "BackgroundSubtractor" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::BackgroundSubtractor >() )    
        .def( 
            "__call__"
            , (void ( ::cv::BackgroundSubtractor::* )( ::cv::Mat const &,::cv::Mat &,double ) )(&::cv::BackgroundSubtractor::operator())
            , (void ( BackgroundSubtractor_wrapper::* )( ::cv::Mat const &,::cv::Mat &,double ) )(&BackgroundSubtractor_wrapper::default___call__)
            , ( bp::arg("image"), bp::arg("fgmask"), bp::arg("learningRate")=0 ) );

}
