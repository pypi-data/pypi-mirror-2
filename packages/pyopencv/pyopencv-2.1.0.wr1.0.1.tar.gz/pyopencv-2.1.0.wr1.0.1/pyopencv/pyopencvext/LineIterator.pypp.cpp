// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "LineIterator.pypp.hpp"

namespace bp = boost::python;

static int get_pixel_addr(cv::LineIterator &inst) { return (int)(*inst); }

static cv::LineIterator & inc(cv::LineIterator &inst) { return ++inst; }

void register_LineIterator_class(){

    bp::class_< cv::LineIterator >( "LineIterator", bp::init< cv::Mat const &, cv::Point, cv::Point, bp::optional< int, bool > >(( bp::arg("img"), bp::arg("pt1"), bp::arg("pt2"), bp::arg("connectivity")=(int)(8), bp::arg("leftToRight")=(bool)(false) )) )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< cv::LineIterator >() )    
        .def_readwrite( "count", &cv::LineIterator::count )    
        .def_readwrite( "err", &cv::LineIterator::err )    
        .def_readwrite( "minusDelta", &cv::LineIterator::minusDelta )    
        .def_readwrite( "minusStep", &cv::LineIterator::minusStep )    
        .def_readwrite( "plusDelta", &cv::LineIterator::plusDelta )    
        .def_readwrite( "plusStep", &cv::LineIterator::plusStep )    
        .def("get_pixel_addr", &get_pixel_addr)    
        .def("inc", bp::make_function(&inc, bp::return_self<>()) );

}
