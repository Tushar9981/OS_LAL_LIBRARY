#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <net/if.h>
#include "oslal.h"

typedef struct {
    const char* dev_name;
    double capacity_mbps;
    double latency_ms;
    double drop_rate;
} network_interface_t;

static network_interface_t ifaces[2] = {
    {"eth0", 40.0, 10.0, 0.01},
    {"wlan0", 30.0, 15.0, 0.05}
};

int oslal_init(void) {
    printf("[OS-LAL Engine] Initialized successfully.\n");
    return 0;
}

int oslal_bind_socket(int socket_fd, oslal_policy_t policy) {
    int best_index = -1;
    double max_utility = -99999.0;

    double W_p = 1.0;
    double W_l = 1.0;
    double W_b = 1.0;
    double W_d = 1.0;

    for (int j = 0; j < 2; j++) {
        if (ifaces[j].capacity_mbps >= policy.req_bandwidth_mbps &&
            ifaces[j].latency_ms <= policy.max_latency_ms) {
            
            double priority_term  = W_p * policy.priority;
            double latency_term   = W_l * (ifaces[j].latency_ms / policy.max_latency_ms);
            double bandwidth_term = W_b * (ifaces[j].capacity_mbps / policy.req_bandwidth_mbps);
            double drop_term      = W_d * ifaces[j].drop_rate;

            double utility = priority_term - latency_term + bandwidth_term - drop_term;

            if (utility > max_utility) {
                max_utility = utility;
                best_index = j;
            }
        }
    }

    if (best_index == -1) {
        printf("[OS-LAL Engine] Error: No interface meets criteria constraints.\n");
        return -1;
    }

    const char* chosen_iface = ifaces[best_index].dev_name;
    printf("[OS-LAL Engine] Binding Socket FD %d -> Interface: %s (Utility: %.2f)\n", 
           socket_fd, chosen_iface, max_utility);

    if (setsockopt(socket_fd, SOL_SOCKET, SO_BINDTODEVICE, chosen_iface, strlen(chosen_iface)) < 0) {
        perror("[OS-LAL Engine] setsockopt SO_BINDTODEVICE failed");
        return -1;
    }

    return 0;
}
