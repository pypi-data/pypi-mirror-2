#include <boost/python.hpp>

#include <Magick++.h>
#include <Magick++/STL.h>

using namespace boost::python;

typedef std::list<Magick::Image> ImageList;

void __STL()
{
    class_< ImageList >("ImageList", init< >())
        .def(init< const ImageList& >())
    ;
}
