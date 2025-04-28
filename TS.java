import java.util.*;

public class TS {

    static class Avion {
        int id;
        int early, ideal, late;
        double earlyPenalty, latePenalty;
        List<Integer> timeDiffs;

        public Avion(int id, int early, int ideal, int late, double earlyPenalty, double latePenalty) {
            this.id = id;
            this.early = early;
            this.ideal = ideal;
            this.late = late;
            this.earlyPenalty = earlyPenalty;
            this.latePenalty = latePenalty;
            this.timeDiffs = new ArrayList<>();
        }

        @Override
        public String toString() {
            return "Avión " + (id + 1) + " Tiempo ideal: " + ideal 
                    + " Penalización temprana: " + earlyPenalty 
                    + " Penalización tardía: " + latePenalty;
        }
    }

    static class Asignacion {
        Avion avion;
        int tiempoAsignado;
    
        public Asignacion(Avion avion, int tiempoAsignado) {
            this.avion = avion;
            this.tiempoAsignado = tiempoAsignado;
        }
    
        @Override
        public String toString() {
            return "Avión " + (avion.id + 1)
                 + " | Ideal: " + avion.ideal
                 + " | Asignado: " + tiempoAsignado
                 + " | EarlyPenalty: " + avion.earlyPenalty
                 + " | LatePenalty: " + avion.latePenalty;
        }
    }
    
    public static void main(String[] args) {
        System.out.println("Mejora-Mejora o Alguna Mejora? (MM/AM): ");
        Scanner scanner = new Scanner(System.in);
        String tipo_busqueda = scanner.nextLine();
        System.out.println("Determinista o Estocástico? (D/E): ");
        String tipo_orden = scanner.nextLine();
        List<Avion> listaOrdenada = Greedy.generarOrdenInicial(listaAviones);

        List<Integer> tabuSizes = List.of(5, 10, 15, 20, 25);
        
    }

    public static List<Asignacion> tabuSearch(List<Asignacion> asignacionesIniciales, int tabuSize, int maxIteraciones) {
        List<Asignacion> solucionActual = new ArrayList<>(asignacionesIniciales);
        List<Asignacion> mejorSolucion = new ArrayList<>(asignacionesIniciales);
        double mejorCosto = calcularCosto(mejorSolucion);
        
        // Lista tabu: movimientos prohibidos (guardamos pares de índices intercambiados)
        LinkedList<String> listaTabu = new LinkedList<>();
        
        int iteracion = 0;
        while (iteracion < maxIteraciones) {
            List<List<Asignacion>> vecinos = buscarVecinos(solucionActual);

            List<Asignacion> mejorVecino = null;
            double mejorCostoVecino = Double.MAX_VALUE;
            String mejorMovimiento = "";

            // Buscar el mejor vecino no tabú o que cumpla el criterio de aspiración
            for (List<Asignacion> vecino : vecinos) {
                double costoVecino = calcularCosto(vecino);
                String movimiento = identificarMovimiento(solucionActual, vecino);

                if (!listaTabu.contains(movimiento) || costoVecino < mejorCosto) {
                    if (costoVecino < mejorCostoVecino) {
                        mejorVecino = vecino;
                        mejorCostoVecino = costoVecino;
                        mejorMovimiento = movimiento;
                    }
                }
            }

            if (mejorVecino == null) {
                // No hay movimiento permitido, terminamos
                break;
            }

            solucionActual = mejorVecino;

            // Actualizamos la lista tabu
            listaTabu.add(mejorMovimiento);
            if (listaTabu.size() > tabuSize) {
                listaTabu.removeFirst(); // eliminamos el más antiguo
            }

            // Actualizar mejor solución encontrada
            if (mejorCostoVecino < mejorCosto) {
                mejorSolucion = mejorVecino;
                mejorCosto = mejorCostoVecino;
            }

            iteracion++;
        }

        return mejorSolucion;
    }

    // Función auxiliar para identificar qué movimiento (swap) se hizo entre dos soluciones
    private static String identificarMovimiento(List<Asignacion> actual, List<Asignacion> vecino) {
        for (int i = 0; i < actual.size(); i++) {
            if (actual.get(i).avion.id != vecino.get(i).avion.id) {
                for (int j = i + 1; j < actual.size(); j++) {
                    if (actual.get(j).avion.id != vecino.get(j).avion.id) {
                        // Registramos los IDs de los aviones intercambiados
                        return actual.get(i).avion.id + "-" + actual.get(j).avion.id;
                    }
                }
            }
        }
        return "";
    }
    
}
