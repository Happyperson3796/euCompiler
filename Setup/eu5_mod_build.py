import eu5.compiler
import sys

print("Running build file in "+sys.argv[-1])
eu5.compiler.Build(sys.argv[-1]).build()