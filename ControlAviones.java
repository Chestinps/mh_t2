import java.io.*;
import java.util.*;

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


        scanner.close();
        
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

            

            List<Avion> ordenInicial = generarOrdenInicial(aviones);
            List<Asignacion> asignacionesIniciales = asignarTiempos(ordenInicial);
            double costoInicial = calcularCosto(asignacionesIniciales);
            System.out.println("Costo inicial: " + costoInicial);

            List<List<Avion>> vecinos = buscarVecinos(ordenInicial);
            for (List<Avion> vecinoOrden : vecinos) {
                List<Asignacion> asignacionesVecino = asignarTiempos(vecinoOrden);
                double costoVecino = calcularCosto(asignacionesVecino);
                //System.out.println("Costo del vecino: " + costoVecino);
                if (costoVecino < costoInicial) {
                    System.out.println("Se encontró un vecino mejor." + " Costo: " + costoVecino);
                    asignacionesIniciales = asignacionesVecino;
                    costoInicial = costoVecino;
                }
            }

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



            

            //-------------------

            
        


            

            
            

            
            

            

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


    // Función para calcular el costo de una lista de aviones
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

    public static List<List<Avion>> buscarVecinos(List<Avion> aviones) {
        List<List<Avion>> vecinos = new ArrayList<>();
        for (int i = 0; i < aviones.size(); i++) {
            for (int j = i + 1; j < aviones.size(); j++) {
                List<Avion> vecino = new ArrayList<>(aviones);
                Collections.swap(vecino, i, j);
                vecinos.add(vecino);
            }
        }
        return vecinos;
    }

    public static List<Avion> generarOrdenInicial(List<Avion> aviones) {
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


    public static List<Asignacion> ordenDeterminista(List<Avion> aviones) {
        aviones.sort((a1, a2) -> {
            double p1 = a1.earlyPenalty + a1.latePenalty;
            double p2 = a2.earlyPenalty + a2.latePenalty;
            if (p1 != p2) {
                return Double.compare(p2, p1);
            } else {
                return Integer.compare(a1.ideal, a2.ideal);
            }
        });
    
        List<Asignacion> asignaciones = new ArrayList<>();
    
        for (int i = 0; i < aviones.size(); i++) {
            Avion avion = aviones.get(i);
    
            int tiempoIdeal = avion.ideal;
            int tiempoMin = avion.early;
            int tiempoMax = avion.late;
    
            int tiempoAterrizaje;
    
            if (i == 0) {
                tiempoAterrizaje = tiempoIdeal;
            } else {
                Avion anterior = asignaciones.get(i - 1).avion;
                int tiempoPrevio = asignaciones.get(i - 1).tiempoAsignado;
                int separacion = anterior.timeDiffs.get(avion.id); // ojo con los índices
                tiempoAterrizaje = Math.max(tiempoIdeal, tiempoPrevio + separacion);
            }
    
            if (tiempoAterrizaje < tiempoMin) tiempoAterrizaje = tiempoMin;
            if (tiempoAterrizaje > tiempoMax) tiempoAterrizaje = tiempoMax;
    
            asignaciones.add(new Asignacion(avion, tiempoAterrizaje));
        }
    
        System.out.println("Asignaciones:");
        for (Asignacion a : asignaciones) {
            System.out.println(a);
        }
    
        return asignaciones;
    }

    public static List<Asignacion> ordenEstocastico(List<Avion> aviones, long seed) {
        List<Avion> copiaAviones = new ArrayList<>(aviones); // para no alterar el orden original
        Random rand = new Random(seed);
        Collections.shuffle(copiaAviones, rand);
    
        List<Asignacion> asignaciones = new ArrayList<>();
    
        for (int i = 0; i < copiaAviones.size(); i++) {
            Avion avion = copiaAviones.get(i);
    
            int tiempoIdeal = avion.ideal;
            int tiempoMin = avion.early;
            int tiempoMax = avion.late;
    
            int tiempoAterrizaje;
    
            if (i == 0) {
                tiempoAterrizaje = tiempoIdeal;
            } else {
                Avion anterior = asignaciones.get(i - 1).avion;
                int tiempoPrevio = asignaciones.get(i - 1).tiempoAsignado;
                int separacion = anterior.timeDiffs.get(avion.id); // cuidado con los índices
                tiempoAterrizaje = Math.max(tiempoIdeal, tiempoPrevio + separacion);
            }
    
            if (tiempoAterrizaje < tiempoMin) tiempoAterrizaje = tiempoMin;
            if (tiempoAterrizaje > tiempoMax) tiempoAterrizaje = tiempoMax;
    
            asignaciones.add(new Asignacion(avion, tiempoAterrizaje));
        }
    
        return asignaciones;
    }

    
    
    public static List<Asignacion> MejorVecino(List<Asignacion> asignaciones) {
        // Obtener todos los vecinos y encontrar el mejor
        List<List<Avion> vecinos = buscarVecinos(asignaciones);
        List<Asignacion> mejorVecino = null;
        double mejorCosto = Double.MAX_VALUE;

        for (List<Asignacion> vecino : vecinos) {
            double costo = calcularCosto(vecino);
            System.out.println("Vecino " + (vecinos.indexOf(vecino) + 1) + " costo: " + costo);
            if (costo < mejorCosto) {
                mejorCosto = costo;
                mejorVecino = vecino;
            }
        }
        return mejorVecino;
    }

    public static List<Asignacion> UnoMejor(List<Asignacion> asignaciones) {
        // Buscar en el vecindario y quedarme con el primero que mejore
        List<List<Asignacion>> vecinos = buscarVecinos(asignaciones);
        List<Asignacion> mejorVecino = null;
        double mejorCosto = calcularCosto(asignaciones);

        for (List<Asignacion> vecino : vecinos) {
            double costo = calcularCosto(vecino);
            if (costo < mejorCosto) {
                mejorCosto = costo;
                mejorVecino = vecino;
                break; // Salir al encontrar el primer vecino que mejora
            }
        }
        return mejorVecino;
    }

    
    
}
