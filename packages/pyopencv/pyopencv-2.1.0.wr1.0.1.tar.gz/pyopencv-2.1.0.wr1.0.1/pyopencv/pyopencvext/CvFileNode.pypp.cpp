// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "boost/python/object.hpp"
#include "CvFileNode.pypp.hpp"

namespace bp = boost::python;

static ::CvTypeInfo * get_info( ::CvFileNode const & inst ) { return inst.info; }

void register_CvFileNode_class(){

    bp::class_< CvFileNode >( "CvFileNode" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvFileNode >() )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvFileNode >() )    
        .def_readwrite( "tag", &CvFileNode::tag )    
        .add_property( "info", bp::make_function(&::get_info, bp::return_internal_reference<>()) );

}
