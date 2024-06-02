#include "contiki.h"
#include "net/netstack.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <math.h>

PROCESS(example_process, "Example process");
AUTOSTART_PROCESSES(&example_process);

#define TX_POWER 0 // puissance de transmission en dbm mais je ne sais pas coment l'adapter

static double calculate_distance(int rssi, int tx_power) {
  // Constantes du modèle de propagation
  double A = 50.0; // Atténuation à 1 mètre
  double n = 2.0;  // Facteur d'atténuation (2 pour un espace libre)
  return pow(10, ((tx_power - rssi) - A) / (10 * n)); //C'est en mètre d'après la formule
}

static void recv_rssi(struct broadcast_conn *c, const linkaddr_t *from) {
  // Pour récup le RRSI
  int rssi = packetbuf_attr(PACKETBUF_ATTR_RSSI);
  printf("Received RSSI from node %d.%d: %ddBm\n", from->u8[0], from->u8[1], rssi);

  double distance = calculate_distance(rssi, TX_POWER);
  printf("Distance to node %d.%d: %.2f meters\n", from->u8[0], from->u8[1], distance);
}

static const struct broadcast_callbacks broadcast_call = {recv_rssi};
static struct broadcast_conn broadcast;

PROCESS_THREAD(example_process, ev, data)
{
  PROCESS_EXITHANDLER(broadcast_close(&broadcast);)
  PROCESS_BEGIN();

  broadcast_open(&broadcast, 129, &broadcast_call);

  while(1) {
    // Autres traitements ici si nécessaire
    PROCESS_WAIT_EVENT();
  }

  PROCESS_END();
}
