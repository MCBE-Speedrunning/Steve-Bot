target := math
objs   := math.o

CC     := gcc
CFLAGS := -O3 -std=c99 -pedantic -Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes -Wno-unused-result

all: $(target)

###
# Automatic dependency tracking
#
deps := $(patsubst %.o,%.d,$(objs))
-include $(deps)
DEPFLAGS = -MMD -MF $(@:.o=.d)

###
# Compile the program
#
$(target): $(objs)
	$(CC) $(CFLAGS) -o $@ $^

%.o: src/%.c
	$(CC) $(CFLAGS) -c $< $(DEPFLAGS)

###
# Phony targets
#
.PHONY: clean
clean:
	rm -f $(target) $(objs) $(deps)
