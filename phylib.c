#include "phylib.h"

// PART 1

// returns a pointer to a new phylib_object which is set as a still ball given a number and position
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{

    phylib_object *newStill = calloc(1, sizeof(phylib_object));

    if (newStill == NULL)
    {

        return NULL;
    }

    newStill->type = PHYLIB_STILL_BALL;
    newStill->obj.still_ball.number = number;
    newStill->obj.still_ball.pos = *pos;

    return newStill;
}

// returns a pointer to a new phylib_object which is set as a rolling ball given a number, position, velocity and acceleration
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{

    phylib_object *newRoll = calloc(1, sizeof(phylib_object));

    if (newRoll == NULL)
    {

        return NULL;
    }

    newRoll->type = PHYLIB_ROLLING_BALL;
    newRoll->obj.rolling_ball.number = number;
    newRoll->obj.rolling_ball.pos = *pos;
    newRoll->obj.rolling_ball.vel = *vel;
    newRoll->obj.rolling_ball.acc = *acc;

    return newRoll;
}

// returns a pointer to a new phylib_object which is set as a hole given a position
phylib_object *phylib_new_hole(phylib_coord *pos)
{

    phylib_object *newHole = calloc(1, sizeof(phylib_object));

    if (newHole == NULL)
    {

        return NULL;
    }

    newHole->type = PHYLIB_HOLE;
    newHole->obj.hole.pos = *pos;

    return newHole;
}

// returns a pointer to a new phylib_object which is set as a horizontal cushion given a y position
phylib_object *phylib_new_hcushion(double y)
{

    phylib_object *newHC = calloc(1, sizeof(phylib_object));

    if (newHC == NULL)
    {

        return NULL;
    }

    newHC->type = PHYLIB_HCUSHION;
    newHC->obj.hcushion.y = y;

    return newHC;
}

// returns a pointer to a new phylib_object which is set as a vertical cushion given an x position
phylib_object *phylib_new_vcushion(double x)
{

    phylib_object *newVC = calloc(1, sizeof(phylib_object));

    if (newVC == NULL)
    {

        return NULL;
    }

    newVC->type = PHYLIB_VCUSHION;
    newVC->obj.vcushion.x = x;

    return newVC;
}

// helper function that creates a new phylib_coord given an x and y value
phylib_coord phylib_new_coord(double x, double y)
{

    phylib_coord newCoord;

    newCoord.x = x;
    newCoord.y = y;

    return newCoord;
}

// returns a pointer to a new pool table with set cushions and holes
phylib_table *phylib_new_table()
{

    phylib_table *newTable = calloc(1, sizeof(phylib_table));

    if (newTable == NULL)
    {

        return NULL;
    }

    phylib_object *holeList[6];

    for (int i = 0; i < 2; i++)
    {

        for (int j = 0; j < 3; j++)
        {

            phylib_coord temp = phylib_new_coord(i * 1350, j * 1350);
            holeList[(i * 3) + j] = phylib_new_hole(&temp);
        }
    }

    newTable->time = 0;
    newTable->object[0] = phylib_new_hcushion(0);
    newTable->object[1] = phylib_new_hcushion(2700);
    newTable->object[2] = phylib_new_vcushion(0);
    newTable->object[3] = phylib_new_vcushion(1350);

    for (int i = 0; i < 6; i++)
    {

        newTable->object[4 + i] = holeList[i];
    }

    return newTable;
}

// PART 2

// returns a copy of a given phylib_object using the given destination pointer
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    if (*src == NULL)
    {
        *dest = NULL;
        return;
    }

    *dest = malloc(sizeof(phylib_object));
    memcpy(*dest, *src, (sizeof(phylib_object)));
}

// returns a pointer to a copy of the given table
phylib_table *phylib_copy_table(phylib_table *table)
{

    phylib_table *newTable = calloc(1, sizeof(phylib_table));

    if (newTable == NULL)
    {

        return NULL;
    }

    newTable->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        phylib_copy_object(&newTable->object[i], &table->object[i]);
    }

    return newTable;
}

// adds a phylib_object to the table
void phylib_add_object(phylib_table *table, phylib_object *object)
{

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        if (table->object[i] == NULL)
        {

            table->object[i] = object;
            break;
        }
    }

    return;
}

// fully frees the given table
void phylib_free_table(phylib_table *table)
{

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        if (table->object[i] != NULL)
        {

            free(table->object[i]);
        }
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        if (table->object[i] != NULL)
        {
        }
    }

    free(table);

    return;
}

// returns a phylib_coord that is the difference of c1 and c2
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{

    phylib_coord sub;

    sub.x = c1.x - c2.x;
    sub.y = c1.y - c2.y;

    return sub;
}

// returns the length of the given phylib_coord
double phylib_length(phylib_coord c)
{

    return sqrt(((c.x) * (c.x) + (c.y) * (c.y)));
    
}

// returns the dot product of phylib_coord a and b
double phylib_dot_product(phylib_coord a, phylib_coord b)
{

    return ((a.x) * (b.x) + (a.y) * (b.y));
}

// returns the distance between 2 phylib_objects (obj1 must be a rolling ball)
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{

    if (obj1->type != PHYLIB_ROLLING_BALL)
    {

        return -1;
    }

    phylib_coord difference;

    // calculate distance from the edge of each object (not the center)
    switch (obj2->type)
    {

    case PHYLIB_STILL_BALL:
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);
        return phylib_length(difference) - PHYLIB_BALL_DIAMETER;

    case PHYLIB_ROLLING_BALL:
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);
        return phylib_length(difference) - PHYLIB_BALL_DIAMETER;

    case PHYLIB_HOLE:
        difference = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);
        return phylib_length(difference) - PHYLIB_HOLE_RADIUS;

    case PHYLIB_HCUSHION:

        return fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;

    case PHYLIB_VCUSHION:

        return fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;

    default:
        return -1;
    }

    // how did we get here?
    return 0;
}

// PART 3

// rolls the given ball for a period of time (new and old objects must be rolling balls)
void phylib_roll(phylib_object *new, phylib_object *old, double time)
{

    // check if both are rolling balls
    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL)
    {

        return;
    }

    // update position and velocity
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x) * time + 0.5 * (old->obj.rolling_ball.acc.x) * time *time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y) * time + 0.5 * (old->obj.rolling_ball.acc.y) * time *time;

    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x *time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y *time;

    // if new and old have velocities in opposing directions, we stopped, set velocity and acceleration to 0
    if (new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x < 0)
    {

        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }

    if (new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y < 0)
    {

        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }

    return;
}

// checks if the given phylib_object has stopped and turns it into a still ball if so (object must be a rolling ball)
unsigned char phylib_stopped(phylib_object *object)
{

    if (fabs(object->obj.rolling_ball.vel.x) < PHYLIB_VEL_EPSILON && fabs(object->obj.rolling_ball.vel.y) < PHYLIB_VEL_EPSILON)
    {

        int tempNum = object->obj.rolling_ball.number;
        phylib_coord tempPos = object->obj.rolling_ball.pos;

        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = tempNum;
        object->obj.still_ball.pos = tempPos;

        return 1;
    }
    else
    {

        return 0;
    }
}

// performs a bounce between 2 phylib_objects (object a must be a rolling ball)
void phylib_bounce(phylib_object **a, phylib_object **b)
{

    phylib_coord tempCoord;
    int tempNum;
    phylib_coord r_ab;
    phylib_coord v_rel;
    double lr_ab;
    phylib_coord n;
    double v_rel_n;
    double a_speed;
    double b_speed;
    double new_a_acc_x;
    double new_a_acc_y;
    double new_b_acc_x;
    double new_b_acc_y;

    switch ((*b)->type)
    {

    // if horizontal cushion hit, invert y acceleration and velocity
    case PHYLIB_HCUSHION:
        (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1;
        (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1;
        break;

    // if vertical cushion hit, invert x acceleration and velocity
    case PHYLIB_VCUSHION:
        (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1;
        (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1;
        break;

    // if a hole is hit, remove the ball from the table
    case PHYLIB_HOLE:
        free(*a);
        *a = NULL;
        break;

    // if a still ball was hit, convert still ball to rolling ball then do calculations for rolling ball bounce
    case PHYLIB_STILL_BALL:
        tempCoord = (*b)->obj.still_ball.pos;
        tempNum = (*b)->obj.still_ball.number;
        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.pos = tempCoord;
        (*b)->obj.rolling_ball.number = tempNum;

    // calculate new velocity and accelerations for both balls
    case PHYLIB_ROLLING_BALL:
        r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
        lr_ab = phylib_length(r_ab);
        n = phylib_new_coord(r_ab.x / lr_ab, r_ab.y / lr_ab);
        v_rel_n = phylib_dot_product(v_rel, n);

        (*a)->obj.rolling_ball.vel.x -= (v_rel_n) * (n.x);
        (*a)->obj.rolling_ball.vel.y -= (v_rel_n) * (n.y);

        (*b)->obj.rolling_ball.vel.x += (v_rel_n) * (n.x);
        (*b)->obj.rolling_ball.vel.y += (v_rel_n) * (n.y);

        a_speed = phylib_length((*a)->obj.rolling_ball.vel);
        b_speed = phylib_length((*b)->obj.rolling_ball.vel);

        if (a_speed > PHYLIB_VEL_EPSILON)
        {

            new_a_acc_x = (-1 * (*a)->obj.rolling_ball.vel.x) / a_speed * PHYLIB_DRAG;
            new_a_acc_y = (-1 * (*a)->obj.rolling_ball.vel.y) / a_speed * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc = phylib_new_coord(new_a_acc_x, new_a_acc_y);
        }

        if (b_speed > PHYLIB_VEL_EPSILON)
        {

            new_b_acc_x = (-1 * (*b)->obj.rolling_ball.vel.x) / b_speed * PHYLIB_DRAG;
            new_b_acc_y = (-1 * (*b)->obj.rolling_ball.vel.y) / b_speed * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc = phylib_new_coord(new_b_acc_x, new_b_acc_y);
        }
    }

    return;
}

// checks the table for the amount of rolling balls present
unsigned char phylib_rolling(phylib_table *t)
{

    unsigned char count = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {

        if (t->object[i] != NULL)
        {

            if (t->object[i]->type == PHYLIB_ROLLING_BALL)
            {
                count++;
            }
        }
    }

    return count;
}

// simulates a segment of a pool shot (returns on ball stop, bounce, or max time is reached for segment)
phylib_table *phylib_segment(phylib_table *table)
{

    double time = PHYLIB_SIM_RATE;
    unsigned char rolling_balls = phylib_rolling(table);

    // check for rolling balls
    if (rolling_balls == 0)
    {

        return NULL;
    }

    phylib_table *new = phylib_copy_table(table);

    // loop check time and rolling balls
    while (time < PHYLIB_MAX_TIME)
    {

        // do phylibsim for the balls
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {

            if (table->object[i] != NULL)
            {

                if (table->object[i]->type == PHYLIB_ROLLING_BALL)
                {

                    phylib_roll(new->object[i], table->object[i], time);

                    if (phylib_stopped(new->object[i]))
                    {
                        new->time += time;
                        return new;
                    }
                }
            }
        }

        // check phylib distance between balls and other objects
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {

            if (new->object[i] != NULL)
            {

                // check if rolling ball
                if (new->object[i]->type == PHYLIB_ROLLING_BALL)
                {

                    // check distance from all objects that are not itself
                    for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
                    {

                        // if distance is 0, perform a bounce then return table
                        if (new->object[i] != NULL &&new->object[j] != NULL && j != i &&phylib_distance(new->object[i], new->object[j]) < 0)
                        {

                            new->time += time;
                            phylib_bounce(&new->object[i], &new->object[j]);

                            if (new->object[i] != NULL &&new->object[i]->type == PHYLIB_ROLLING_BALL)
                            {

                                phylib_stopped(new->object[i]);
                            }

                            if (new->object[j] != NULL &&new->object[j]->type == PHYLIB_ROLLING_BALL)
                            {

                                phylib_stopped(new->object[j]);
                            }

                            return new;
                        }
                    }
                }
            }
        }

        // check for rolling balls again (in case of a weird perfect collision)
        if (phylib_rolling(new) == 0)
        {
            phylib_free_table(new);
            return NULL;
        }

        time += PHYLIB_SIM_RATE;
    }

    // if max time is reached, there is an error
    if (time >= PHYLIB_MAX_TIME)
    {
        printf("Max time was reached\n");
    }

    new->time += time;
    return new;
}

char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}
