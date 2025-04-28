import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class ControlAviones {

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
        Scanner scanner = new Scanner(System.in);

        System.out.print("Bienvenido al Control de Aviones, escoja el caso que desea ejecutar: ");
        String file = scanner.nextLine();

        System.out.print("¿Usar Best Improvement? (true/false): ");
        boolean usarBestImprovement = scanner.nextBoolean();
        
        scanner.close();
        

        // Lectura de los archivos
        String chosenFile;
        switch (file) {
            case "1" -> chosenFile = "case1.txt";
            case "2" -> chosenFile = "case2.txt";
            case "3" -> chosenFile = "case3.txt";
            case "4" -> chosenFile = "case4.txt";
            default -> {
                System.out.println("Opción no válida.");
                return;
            }
        }

        try (BufferedReader br = new BufferedReader(new FileReader(chosenFile))) {
            int numAviones = Integer.parseInt(br.readLine().trim());
            List<Avion> aviones = new ArrayList<>();

            for (int i = 0; i < numAviones; i++) {
                String[] info = br.readLine().trim().split("\\s+");
                Avion a = new Avion(i, Integer.parseInt(info[0]), Integer.parseInt(info[1]),
                        Integer.parseInt(info[2]), Double.parseDouble(info[3]), Double.parseDouble(info[4]));

                while (a.timeDiffs.size() < numAviones - 1) {
                    String[] values = br.readLine().trim().split("\\s+");
                    for (String val : values) {
                        a.timeDiffs.add(Integer.parseInt(val));
                    }
                }
                aviones.add(a);
            }

            
            
            List<Avion> ordenInicial = ordenDeterminista(aviones);
            List<Asignacion> asignacionesIniciales = asignarTiempos(ordenInicial);

            List<Asignacion> solucion = buscarMejorSolucion(asignacionesIniciales, usarBestImprovement);

            System.out.println("Costo final: " + calcularCosto(solucion));

            
            
            long seed = 18042025;
            Random rng = new Random(seed);
            
            
            System.out.println("\nResultados estocásticos:");
            for (int i = 0; i < 10; i++) {
                System.out.print((i + 1) + ": ");
                List<Asignacion> asignacionesEstocasticas = ordenEstocastico(aviones, rng.nextLong());
                double costoEstocastico = calcularCosto(asignacionesEstocasticas);
                System.out.println("Costo estocástico inicial: " + costoEstocastico);
                List<Asignacion> mejorVecino = MejorVecino(asignacionesEstocasticas);
                double costoMejorVecino = calcularCosto(mejorVecino);
                System.out.println("Costo Mejor Vecino: " + costoMejorVecino);
                List<Asignacion> unoMejor = UnoMejor(asignacionesEstocasticas);
                double costoUnoMejor = calcularCosto(unoMejor);
                System.out.println("Costo Uno Mejor: " + costoUnoMejor);
            }

            

        } catch (IOException | NumberFormatException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    

    public static void imprimirAviones(List<Avion> aviones) {
        for (Avion avion : aviones) {
            System.out.println(avion);
        }
    }

    public static void imprimirAsignaciones(List<Asignacion> asignaciones) {
        for (Asignacion asignacion : asignaciones) {
            System.out.println(asignacion);
        }
    }
    

    //+---------------------+
    //+-------Greedy--------+
    //+---------------------+

    public static List<Avion> ordenDeterminista(List<Avion> aviones) {
        aviones.sort((a1, a2) -> {
            double p1 = a1.earlyPenalty + a1.latePenalty;
            double p2 = a2.earlyPenalty + a2.latePenalty;
            if (p1 != p2) {
                return Double.compare(p2, p1);
            } else {
                return Integer.compare(a1.ideal, a2.ideal);
            }
        });
        return aviones;
    }


    public static List<Asignacion> ordenEstocastico(List<Avion> aviones, long seed) {
        List<Avion> copiaAviones = new ArrayList<>(aviones); // Para no alterar el orden original
        Random rand = new Random(seed);
        Collections.shuffle(copiaAviones, rand);
    
        List<Asignacion> asignaciones = new ArrayList<>();
    
        for (int i = 0; i < copiaAviones.size(); i++) {
            Avion avion = copiaAviones.get(i);
            Asignacion anterior = (i == 0) ? null : asignaciones.get(i - 1);
            int tiempo = calcularTiempo(avion, anterior);
            asignaciones.add(new Asignacion(avion, tiempo));
        }
    
        return asignaciones;
    }

    private static int calcularTiempo(Avion actual, Asignacion anterior) {
        int tiempoIdeal = actual.ideal;
        int tiempoMin = actual.early;
        int tiempoMax = actual.late;
        
        if (anterior == null) {
            return tiempoIdeal;
        }
    
        int tiempoPrevio = anterior.tiempoAsignado;
        int separacion = anterior.avion.timeDiffs.get(actual.id);
        int tiempoAterrizaje = Math.max(tiempoIdeal, tiempoPrevio + separacion);
    
        return Math.min(Math.max(tiempoAterrizaje, tiempoMin), tiempoMax);
    }
    
    public static List<Asignacion> asignarTiempos(List<Avion> aviones) {
        List<Asignacion> asignaciones = new ArrayList<>();
        for (int i = 0; i < aviones.size(); i++) {
            Avion avion = aviones.get(i);
            Asignacion anterior = (i == 0) ? null : asignaciones.get(i - 1);
            int tiempo = calcularTiempo(avion, anterior);
            asignaciones.add(new Asignacion(avion, tiempo));
        }
        return asignaciones;
    }

    //+---------------------+
    //+--------GRASP--------+
    //+---------------------+


    public static List<Asignacion> buscarMejorSolucion(List<Asignacion> asignacionesIniciales, boolean usarBestImprovement) {
        List<Asignacion> asignacionesActuales = new ArrayList<>(asignacionesIniciales);
        double costoActual = calcularCosto(asignacionesActuales);
        boolean mejora = true;
    
        while (mejora) {
            mejora = false;
            List<Asignacion> mejorVecino;
    
            if (usarBestImprovement) {
                mejorVecino = MejorVecino(asignacionesActuales);
            } else {
                mejorVecino = UnoMejor(asignacionesActuales);
            }
    
            if (mejorVecino != null) {
                double costoVecino = calcularCosto(mejorVecino);
                if (costoVecino < costoActual) {
                    asignacionesActuales = mejorVecino;
                    costoActual = costoVecino;
                    mejora = true;
                }
            }
        }
    
        return asignacionesActuales;
    }

    
    
    public static List<Asignacion> MejorVecino(List<Asignacion> asignacionesActuales) {
        List<Asignacion> mejorAsignacion = null;
        double mejorCosto = calcularCosto(asignacionesActuales);
        List<List<Asignacion>> vecinos = buscarVecinos(asignacionesActuales);
    
        for (List<Asignacion> vecino : vecinos) {
            double costoVecino = calcularCosto(vecino);
            if (costoVecino < mejorCosto) {
                mejorCosto = costoVecino;
                mejorAsignacion = vecino;
            }
        }
        return mejorAsignacion; // puede retornar null si no hay mejora
    }
    
    public static List<Asignacion> UnoMejor(List<Asignacion> asignacionesActuales) {
        List<List<Asignacion>> vecinos = buscarVecinos(asignacionesActuales);
        double costoActual = calcularCosto(asignacionesActuales);
    
        for (List<Asignacion> vecino : vecinos) {
            double costoVecino = calcularCosto(vecino);
            if (costoVecino < costoActual) {
                return vecino;
            }
        }
        return null; // no encontró ningún vecino mejor
    }

    public static double calcularCosto(List<Asignacion> asignaciones) {
        double costoTotal = 0.0;
        for (Asignacion asignacion : asignaciones) {
            Avion avion = asignacion.avion;
            int tiempoAsignado = asignacion.tiempoAsignado;
    
            if (tiempoAsignado < avion.ideal) {
                costoTotal += avion.earlyPenalty * (avion.ideal - tiempoAsignado);
            } else if (tiempoAsignado > avion.ideal) {
                costoTotal += avion.latePenalty * (tiempoAsignado - avion.ideal);
            }
        }
        return costoTotal;
    }

    public static List<List<Asignacion>> buscarVecinos(List<Asignacion> asignaciones) {
        List<List<Asignacion>> vecinos = new ArrayList<>();
        for (int i = 0; i < asignaciones.size(); i++) {
            for (int j = i + 1; j < asignaciones.size(); j++) {
                // Crear una nueva lista con el mismo orden de aviones
                List<Avion> orden = new ArrayList<>();
                for (Asignacion asignacion : asignaciones) {
                    orden.add(asignacion.avion);
                }
    
                // Hacer swap en el orden de los aviones
                Collections.swap(orden, i, j);
    
                // Volver a calcular tiempos basados en el nuevo orden
                List<Asignacion> vecino = asignarTiempos(orden);
    
                // Agregar el nuevo vecino
                vecinos.add(vecino);
            }
        }
        return vecinos;
    }

    //+---------------------+
    //+-----Tabu Search-----+
    //+---------------------+


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
