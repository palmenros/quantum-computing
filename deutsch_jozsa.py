import matplotlib.pyplot as plt
import qiskit.visualization
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.basicaer import QasmSimulatorPy

from qiskit.circuit.classicalfunction import classical_function
from qiskit.circuit.classicalfunction.types import Int1


@classical_function
def oracle_function(a : Int1, b : Int1, c: Int1) -> Int1:
    # return (a xor b) and c
    a_xor_b = (a and not b) or (not a and b)
    return (a_xor_b and not c) or (not a_xor_b and c)


# Number of inputs that the classicacl function has
n = len(oracle_function.args)

# Create a Quantum Circuit acting on a quantum register of three qubits
q_reg = QuantumRegister(n+1, 'q')
c_reg = ClassicalRegister(n, 'c')
circ = QuantumCircuit(q_reg, c_reg)

# Initialize q_reg[n] to 1
circ.x(q_reg[n])

circ.barrier()

for i in range(n+1):
    circ.h(i)

circ.barrier()

circ.append(oracle_function, q_reg)

circ.barrier()


for i in range(n):
    circ.h(i)

circ.measure(q_reg[:n], c_reg)

circ.draw('mpl')

print(circ.qasm())

simulator = QasmSimulatorPy()
compiled_circuit = transpile(circ, simulator)

job = simulator.run(compiled_circuit, shots=1000)
result = job.result()

counts = result.get_counts(circ)

print("\nTotal count are:", counts)
qiskit.visualization.plot_histogram(counts)
plt.show()
