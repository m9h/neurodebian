/* Force-included via DEB_CXXFLAGS_MAINT_APPEND when compiling ACVD's own
 * sources: they use unqualified cout/cerr/endl without <iostream> or a using
 * directive, relying on transitive includes that newer VTK no longer provides. */
#include <iostream>
using namespace std;
