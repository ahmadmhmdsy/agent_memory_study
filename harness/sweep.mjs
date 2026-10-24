// Remove every study container (label r013=1) a crashed or stopped run left behind.
import { sweepContainers } from "./runtime.mjs";
console.log(`removed ${await sweepContainers()} container(s)`);
