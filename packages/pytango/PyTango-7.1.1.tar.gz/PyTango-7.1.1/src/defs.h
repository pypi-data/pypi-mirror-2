#pragma once

#include <string>
#include <vector>

typedef std::vector<std::string> StdStringVector;
typedef std::vector<long> StdLongVector;
typedef std::vector<double> StdDoubleVector;

namespace PyTango
{
    enum ExtractAs {
        ExtractAsNumpy,
        ExtractAsTuple,
        ExtractAsList,
        ExtractAsString,
        ExtractAsPyTango3,
        ExtractAsNothing
    };
}
