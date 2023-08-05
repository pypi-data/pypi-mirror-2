// This file has been generated by Py++.

#include "boost/python.hpp"
#include "__ctypes_integration.pypp.hpp"
#include "opencv_headers.hpp"
#include "boost/python/object.hpp"
#include "boost/python/list.hpp"
#include "boost/python/tuple.hpp"
#include "CvHaarStageClassifier.pypp.hpp"

namespace bp = boost::python;

static bp::object get_classifier( ::CvHaarStageClassifier const & inst ){
    bp::list l;
    for(int i = 0; i < inst.count; ++i)
        l.append(inst.classifier[i]);
    return bp::tuple(l);
}

void register_CvHaarStageClassifier_class(){

    bp::class_< CvHaarStageClassifier >( "CvHaarStageClassifier" )    
        .add_property( "this", pyplus_conv::make_addressof_inst_getter< CvHaarStageClassifier >() )    
        .def_readwrite( "child", &CvHaarStageClassifier::child )    
        .def_readwrite( "count", &CvHaarStageClassifier::count )    
        .def_readwrite( "next", &CvHaarStageClassifier::next )    
        .def_readwrite( "parent", &CvHaarStageClassifier::parent )    
        .def_readwrite( "threshold", &CvHaarStageClassifier::threshold )    
        .add_property( "classifier", &::get_classifier );

}
