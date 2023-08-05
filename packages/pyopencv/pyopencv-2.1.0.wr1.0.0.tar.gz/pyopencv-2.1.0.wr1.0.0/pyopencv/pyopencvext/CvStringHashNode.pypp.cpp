// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "boost/python/object.hpp"
#include "CvStringHashNode.pypp.hpp"

namespace bp = boost::python;

static ::CvStringHashNode * get_next( ::CvStringHashNode const & inst ) { return inst.next; }

void register_CvStringHashNode_class(){

    bp::class_< CvStringHashNode >( "CvStringHashNode" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvStringHashNode >() )    
        .def_readwrite( "hashval", &CvStringHashNode::hashval )    
        .def_readwrite( "str", &CvStringHashNode::str )    
        .add_property( "next", bp::make_function(&::get_next, bp::return_internal_reference<>()) );

}
