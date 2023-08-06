/*
 +-----------------------------------------------------------+
 * @desc	Generic list type
 * @file	llist_t.c
 * @package RLF
 * @license FIXME
 * <jtm@robot.is>
 +-----------------------------------------------------------+
 */
#include "headers/rlf.h"

static void RLF_list_allocate_int(RLF_list_t l);

/*
 +-----------------------------------------------------------+
 * @desc	Create new empty list
 +-----------------------------------------------------------+
 */
RLF_list_t
RLF_list_create(void) {
	return (RLF_list_t)calloc(1, sizeof(list_t));
}
/*
 +-----------------------------------------------------------+
 * @desc	Create new empty list of a certain size
 +-----------------------------------------------------------+
 */
RLF_list_t
RLF_list_create_size(const int size) {
	RLF_list_t l = RLF_list_create();
	if(size <= 1) return l;
	LIST(l)->data = (void **)calloc(sizeof(void *), size);
	LIST(l)->asize = size;
	return l;
}
/*
 +-----------------------------------------------------------+
 * @desc	Append element to list
 +-----------------------------------------------------------+
 */
void
RLF_list_append(RLF_list_t l, const void * element) {
	if(!l) return;
	if (LIST(l)->fsize+1 >= LIST(l)->asize)
		RLF_list_allocate_int(l);
	LIST(l)->data[LIST(l)->fsize++] = (void *)element;
}
/*
 +-----------------------------------------------------------+
 * @desc	Pop item off list
 +-----------------------------------------------------------+
 */
void *
RLF_list_pop(RLF_list_t l) {
	if(!l) return NULL;
	if(LIST(l)->fsize >= 0)
		return NULL;
	return LIST(l)->data[--(LIST(l)->fsize)];
}
/*
 +-----------------------------------------------------------+
 * @desc	Extend list with other list
 +-----------------------------------------------------------+
 */
void
RLF_list_extend(RLF_list_t l, RLF_list_t l2) {
	if(!l || !l2)
		return;
	void **i;
	for (i = RLF_list_begin(l2); i != RLF_list_end(l2); i++) {
		RLF_list_append(l, *i);
	}
}
/*
 +-----------------------------------------------------------+
 * @desc	Get element at location
 +-----------------------------------------------------------+
 */
void *
RLF_list_get(RLF_list_t l, unsigned int index) {
	if(!l || index > (LIST(l)->fsize))
		return NULL;
	return LIST(l)->data[index];
}
/*
 +-----------------------------------------------------------+
 * @desc	Set element at location
 +-----------------------------------------------------------+
 */
void
RLF_list_set(RLF_list_t l, unsigned int index, const void * element) {
	if(!l) return;
	while(LIST(l)->asize < index + 1)
		RLF_list_allocate_int(l);
	LIST(l)->data[index] = (void *)element;
	if (index + 1 > LIST(l)->fsize)
		LIST(l)->fsize = index+1;
}
/*
 +-----------------------------------------------------------+
 * @desc	Return pointer to first element
 +-----------------------------------------------------------+
 */
void **
RLF_list_begin(RLF_list_t l) {
	if(!l) return NULL;
	if (LIST(l)->fsize == 0)
		return (void **)NULL;
	return &LIST(l)->data[0];
}
/*
 +-----------------------------------------------------------+
 * @desc	Return pointer to last element
 +-----------------------------------------------------------+
 */
void **
RLF_list_end(RLF_list_t l) {
	if(!l) return NULL;
	if (LIST(l)->fsize == 0)
		return (void **)NULL;
	return &LIST(l)->data[LIST(l)->fsize];
}
/*
 +-----------------------------------------------------------+
 * @desc	Insert element before index
 +-----------------------------------------------------------+
 */
void **
RLF_list_insert(RLF_list_t l, const void *element, int before) {
	int idx;
	if(!l) return NULL;
	if (LIST(l)->fsize + 1 >= LIST(l)->asize)
		RLF_list_allocate_int(l);
	for (idx=LIST(l)->fsize; idx > before; idx--) {
		LIST(l)->data[idx] = LIST(l)->data[idx-1];
	}
	LIST(l)->data[before] = (void *)element;
	LIST(l)->fsize++;
	return &LIST(l)->data[before];
}
/*
 +-----------------------------------------------------------+
 * @desc	List size
 +-----------------------------------------------------------+
 */
int
RLF_list_size(RLF_list_t l) {
	if(!l) return 0;
	return LIST(l)->fsize;
}
/*
 +-----------------------------------------------------------+
 * @desc	Empty list
 +-----------------------------------------------------------+
 */
void
RLF_list_empty(RLF_list_t l) {
	if(!l) return;
	LIST(l)->fsize=0;
}
/*
 +-----------------------------------------------------------+
 * @desc	Delete list
 +-----------------------------------------------------------+
 */
void RLF_list_delete(RLF_list_t l) {
	if(!l) return;
	if(LIST(l)->data) free(LIST(l)->data);
	free(l);
}
/*
 +-----------------------------------------------------------+
 * @desc	FIXME
 +-----------------------------------------------------------+
 */
void **
RLF_list_remove_iterator(RLF_list_t l, void ** element) {
	void **e;
	if(!l || !element)
		return NULL;
	for(e = element; e < RLF_list_end(l) - 1; e++) {
		*e = *(e+1);
	}
	LIST(l)->fsize--;
	if(LIST(l)->fsize == 0)
		return ((void **)NULL)-1;
	return element - 1;
}
/*
 +-----------------------------------------------------------+
 * @desc	"Grow" list, doubleing its size
 +-----------------------------------------------------------+
 */
static void
RLF_list_allocate_int(RLF_list_t l) {
	void **new;
	int nsize = LIST(l)->asize * 2;
	if (nsize == 0) nsize = 16;
	new = (void **)calloc(sizeof(void *), nsize);
	if (LIST(l)->data) {
		if (LIST(l)->fsize > 0)
			memcpy(new, LIST(l)->data, sizeof(void *)*LIST(l)->fsize);
		free(LIST(l)->data);
	}
	LIST(l)->asize = nsize;
	LIST(l)->data = new;
}


