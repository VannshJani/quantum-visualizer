import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector, circuit_drawer
import numpy as np
from io import BytesIO
from PIL import Image


def get_bloch_sphere(quantum_state_vector):
    # Plot Bloch sphere for quantum state
    return plot_bloch_multivector(quantum_state_vector)

def get_circuit_image(circuit):
    # Render circuit to an image
    img_stream = BytesIO()
    circuit_drawer(circuit, output='mpl').savefig(img_stream, format='png')
    img_stream.seek(0)
    return img_stream

def change_initial_values(quantum_state_vector):
    st.session_state.initial_circuit = QuantumCircuit(1)
    st.session_state.initial_vector = quantum_state_vector


st.title("Single Qubit Quantum Circuit Builder")

# Initialize session state variables
if 'is_initialized' not in st.session_state:
    st.session_state.is_initialized = False
if 'initial_circuit' not in st.session_state:
    st.session_state.initial_circuit = QuantumCircuit(1)
if 'initial_vector' not in st.session_state:
    st.session_state.initial_vector = np.array([1, 0])
if 'qc' not in st.session_state:
    st.session_state.qc = st.session_state.initial_circuit.copy()
if 'quantum_state_vector' not in st.session_state:
    st.session_state.quantum_state_vector = st.session_state.initial_vector.copy()

# Sidebar - Gate Options
st.sidebar.header("Add Gates")
if st.sidebar.button("Add Hadamard"):
    st.session_state.qc.h(0)
    st.session_state.is_initialized = True
if st.sidebar.button("Add Pauli-X"):
    st.session_state.qc.x(0)
    st.session_state.is_initialized = True
if st.sidebar.button("Add Pauli-Y"):
    st.session_state.qc.y(0)
    st.session_state.is_initialized = True
if st.sidebar.button("Add Pauli-Z"):
    st.session_state.qc.z(0)
    st.session_state.is_initialized = True
if st.sidebar.button("Add S"):
    st.session_state.qc.s(0)
    st.session_state.is_initialized = True
if st.sidebar.button("Add T"):
    st.session_state.qc.t(0)
    st.session_state.is_initialized = True

st.write("Added Gate to Circuit")

# # Change initial values
# if st.sidebar.button("Change Initial Values"):
#     vector_input = st.sidebar.text_input("Enter Quantum State Vector (comma separated)", value="1,0")
#     st.session_state.quantum_state_vector = np.array([float(x) for x in vector_input.split(",")])
#     change_initial_values(st.session_state.quantum_state_vector)

# Reset Circuit
if st.sidebar.button("Reset Circuit"):
    st.session_state.qc = QuantumCircuit(1)
    st.session_state.quantum_state_vector = np.array([1, 0])
    st.session_state.is_initialized = False

# Transpile and simulate quantum state
if st.session_state.is_initialized:
    simulator = Aer.get_backend('statevector_simulator')
    transpiled_qc = transpile(st.session_state.qc, simulator)
    result = simulator.run(transpiled_qc).result()
    st.session_state.quantum_state_vector = result.get_statevector()

# Layout - Display Bloch Sphere and Circuit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bloch Sphere")
    fig = get_bloch_sphere(st.session_state.quantum_state_vector)
    st.pyplot(fig)

with col2:
    st.subheader("Quantum Circuit")
    circuit_img = get_circuit_image(st.session_state.qc)
    st.image(circuit_img, caption="Quantum Circuit", use_column_width=True)
    
    # Display Quantum State Vector
    st.subheader("Quantum State Vector")
    # write value of quantum state vector
    zero = "$\ket{0}$"
    one = "$\ket{1}$"
    if st.session_state.is_initialized:
        st.write("$\quad$ $\ket{q}$ = ", round(st.session_state.quantum_state_vector[0],3),zero,"+",round(st.session_state.quantum_state_vector[1],3),one)
        
    else:
        st.write("$\quad$ $\ket{q}$ = ",zero)
