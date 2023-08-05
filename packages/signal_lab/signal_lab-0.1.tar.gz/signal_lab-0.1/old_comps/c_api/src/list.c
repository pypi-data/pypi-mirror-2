
#include <string.h>
#include <stdlib.h>

#include <slab/list.h>

StringList slab_list_allocate( )
{
	return  (StringList) malloc(sizeof(struct StringListStruct) );
}

void slab_list_init( StringList slist )
{
	slist->mem_len = 8;
	slist->len = 0;
	slist->lst = malloc( sizeof(char*) * slist->mem_len );

//	slist->next = 0;
//	strcpy(slist->str ,str );
}

void slab_list_init1( StringList slist, int size )
{
	slist->mem_len = size;
	slist->len = 0;
	slist->lst = malloc( sizeof(char*) * slist->mem_len );

}

void slab_list_expand( StringList slist )
{
	slist->mem_len *= 2;
	slist->lst = realloc( slist->lst, sizeof(char*) * slist->mem_len );
}



StringList slab_list_create(  )
{
//	void* p = malloc(sizeof(struct Dictionary) );
	StringList slist = slab_list_allocate( );

	slab_list_init( slist );
	return slist;
}

void slab_list_delete( StringList sl )
{
	int i;
	for ( i=0; i< sl->len; i++ )
	{
		free( sl->lst[i] );
	}

	free( sl->lst );

//	if ( sl == 0 )
//		return;
//	else if (sl != sl->next )
//	{
//		if ( sl->next != 0 )
//		{
//			slab_list_delete( sl->next );
//			sl->next = 0;
//		}
//		free( sl );
//	}
}

StringList slab_list_copy( StringList sl )
{
	if (sl==0)
		return 0;

	StringList new = slab_list_allocate(  );

	slab_list_init1( new, sl->mem_len );

	new->len= sl->len;
	new->mem_len= sl->mem_len;

	int i;
	for ( i=0; i< sl->len; i++ )
	{
		new->lst[i] = malloc( sizeof(char) * strlen( sl->lst[i] )+1 );
		strcpy( new->lst[i], sl->lst[i]);
	}

	return new;
}

void slab_list_append( StringList sl, const char* value )
{

	if (sl->len == sl->mem_len )
	{
		slab_list_expand( sl );
	}

	sl->lst[sl->len] = malloc( strlen( value )+1 );
	strcpy( sl->lst[sl->len], value );

	sl->len++;

//	StringList curr = sl;
//
//	while ( curr->next != 0 )
//	{
//		curr = curr->next;
//	}
//
//	StringList last = slab_list_create( value );
//	curr->next = last;

}

int slab_list_len( StringList sl )
{
	return sl->len;
//	int ctr=1;
//	StringList curr = sl;
//
//	if ( curr==0)
//		return 0;
//
//	while ( curr->next != 0 )
//	{
//		ctr++;
//		curr = curr->next;
//	}
//
//	return ctr;

}

char** slab_list_flatten( StringList sl, int* len )
{
	*len = slab_list_len(sl);
	return sl->lst;
//	int length = slab_list_len( sl );
//	*len = length;
//
//	if (length==0)
//		return 0;
//
//	char** ptr = (char**) malloc( length );
//	char** ret= (char**) ptr;
//
//	StringList curr = sl;
//
//	while ( curr != 0 )
//	{
//		*ptr = curr->str;
//		curr = curr->next;
//		ptr++;
//	}
//
//
//	return ret;

}


char* slab_list_get( StringList sl, unsigned int idx)
{
	if (idx >= sl->len )
	{
		return 0;
	}
	return sl->lst[idx];
//	StringList curr = sl;
//	int ctr=0;
//
//	while ( curr!=0 )
//	{
//		if (ctr==idx)
//			return curr->str;
//		ctr++;
//		curr = curr->next;
//	}
//
//	return 0;
}
