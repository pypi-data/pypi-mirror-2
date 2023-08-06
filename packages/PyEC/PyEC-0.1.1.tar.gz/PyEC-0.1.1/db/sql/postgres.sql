-- CREATE USER pyec WITH PASSWORD 'pyec';

-- CREATE DATABASE pyec WITH OWNER=pyec;

-- \c pyec



CREATE OR REPLACE FUNCTION update_prob_index(mult double precision, diff double precision, div double precision, seg integer) RETURNS integer AS $$
DECLARE
   tot double precision;
   score double precision;
   count integer;
   ident integer;
   incr double precision;
   total double precision;
   mx double precision;
BEGIN
   SELECT totalProb INTO total FROM db_segment WHERE id = seg;
   IF total = 0.0 THEN 
      total := 1e-100;
   END IF;
   tot := 0;
   SELECT max(score) INTO mx FROM db_point WHERE segment_id=seg;
   FOR ident, score, count IN SELECT gp.id, gp.score, gp.count FROM db_point as gp WHERE gp.segment_id=seg AND gp.alive ORDER BY gp.id LOOP
      BEGIN
          incr := exp((score - diff) * mult) / (count * div);
          IF incr / total < 1e-10 and score < mx THEN
             DELETE FROM db_distance WHERE fro_id=ident or to_id=ident;
             --DELETE FROM db_point WHERE id=ident;   
             UPDATE db_point SET alive=false WHERE id=ident;
          ELSE
             tot := tot + incr;
          END IF;
      EXCEPTION
          WHEN FLOATING_POINT_EXCEPTION THEN tot := tot;
          WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN tot := tot;
          WHEN DATA_EXCEPTION THEN tot := tot;
      END;
      UPDATE db_point SET probindex = tot where id = ident;
   END LOOP;
   
   UPDATE db_segment SET totalprob = tot WHERE id = seg;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_prob_index_partition(mult double precision, diff double precision, div double precision, seg integer) RETURNS integer AS $$
DECLARE
   tot double precision;
   score double precision;
   area double precision;
   ident integer;
   incr double precision;
   total double precision;
   mx double precision;
BEGIN
   SELECT totalProb INTO total FROM db_segment WHERE id = seg;
   IF total = 0.0 THEN 
      total := 1e-100;
   END IF;
   tot := 0;
   SELECT max(score) INTO mx FROM db_point WHERE segment_id=seg;
   FOR ident, score, area IN SELECT gp.id, gp.score, gr.area FROM db_point as gp INNER JOIN db_partition as gr ON gr.point_id=gp.id WHERE gp.segment_id=seg AND gp.alive ORDER BY gp.id LOOP
      BEGIN
          incr := exp((score - diff) * mult) * area / div;
          tot := tot + incr;
      EXCEPTION
          WHEN FLOATING_POINT_EXCEPTION THEN tot := tot;
          WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN tot := tot;
          WHEN DATA_EXCEPTION THEN tot := tot;
      END;
      UPDATE db_point SET probindex = tot where id = ident;
   END LOOP;
   
   UPDATE db_segment SET totalprob = tot WHERE id = seg;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_prob_index_sharpen(multIncr float, seg integer) RETURNS integer AS $$
DECLARE
   tot float;
   score float;
   cnt2 integer;
   ident integer;
   cnt integer;
   mult float;
   div float;
   average float;
   incr float;
   total float;
   mx float;
   curs3 CURSOR FOR SELECT COALESCE(COUNT(id),0) FROM db_point WHERE  segment_id = seg;
   curs4 CURSOR FOR SELECT COALESCE(AVG(score),0) FROM db_point WHERE segment_id = seg;
BEGIN
   OPEN curs3;
   FETCH curs3 INTO cnt;
   CLOSE curs3;
   OPEN curs4;
   FETCH curs4 INTO average;
   CLOSE curs4;
   mult := multIncr * cnt;
   div = exp(average*mult);
   tot := 0;
   SELECT max(score) INTO mx FROM db_point WHERE segment_id=seg;
   SELECT totalProb INTO total FROM db_segment WHERE id = seg;
   IF total = 0.0 THEN total := 1e-100; END IF;
   FOR ident, score, cnt2 IN SELECT gp.id, gp.score, gp.count FROM db_point as gp  WHERE gp.segment_id=seg AND gp.alive ORDER BY gp.id LOOP
      BEGIN
          incr := exp(score * mult) / (div * cnt2);
          tot := tot + incr;
          IF incr / total < 1e-10  and score < mx THEN
             DELETE FROM db_distance WHERE fro_id=ident or to_id=ident;
             --DELETE FROM db_point WHERE id=ident;
             UPDATE db_point SET alive=false WHERE id=ident;
          ELSE
             tot := tot + incr;   
          END IF;
          
      EXCEPTION
          WHEN FLOATING_POINT_EXCEPTION THEN tot := tot;
          WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN tot := tot;
          WHEN DATA_EXCEPTION THEN tot := tot;
      END;
      UPDATE db_point SET probindex = tot where id = ident;
   END LOOP;
   
   UPDATE db_segment SET totalprob = tot WHERE id = seg;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_prob_index_normal(seg integer) RETURNS integer AS $$
DECLARE
   tot real;
   score real;
   minScore real;
   count integer;
   ident integer;
   incr float;
   total float;
   mx float;
BEGIN
   SELECT max(score) INTO mx FROM db_point WHERE segment_id=seg;
   minScore := 0;
   SELECT min(score) INTO minScore FROM db_point WHERE segment_id = seg;
   SELECT totalProb INTO total FROM db_segment WHERE id = seg;
   IF total = 0.0 THEN total := 1e-100; END IF;
   minScore := COALESCE(minScore, -1);
   tot := 0;
   FOR ident, score, count IN SELECT gp.id, gp.score, gp.count FROM db_point as gp WHERE gp.segment_id=seg AND gp.alive ORDER BY gp.id LOOP
      incr := (score - minScore + 1) / count;
      IF incr / total < 1e-10 and score < mx THEN
         DELETE FROM db_distance WHERE fro_id=ident or to_id=ident;
         --DELETE FROM db_point WHERE id=ident;   
         UPDATE db_point SET alive=false WHERE id=ident;
      ELSE
         tot := tot + incr;
      END IF;
      UPDATE db_point SET probindex = tot where id = ident;
   END LOOP;
   
   UPDATE db_segment SET totalprob = tot WHERE id = seg;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION distance(x real[], y real[]) RETURNS real AS $$
DECLARE
   currx real;
   curry real;
   sq real;
   sum real;
   curs2 CURSOR FOR SELECT unnest(y);
BEGIN
   sum := 0;
   OPEN curs2;
   FOR currx IN SELECT unnest(x) LOOP
      FETCH curs2 INTO curry;
      sq = currx - curry;
      sq = sq * sq;
      sum = sum + sq;
   END LOOP;
   CLOSE curs2;
   sum = SQRT(sum);
   RETURN sum;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_distances(seg integer) RETURNS integer AS $$
DECLARE
   id1 integer;
   id2 integer;
   point1 real[];
   point2 real[];
   dist real;
BEGIN
   FOR id1, point1 IN SELECT gp.id, gp.point FROM db_point AS gp LEFT JOIN db_distance AS gd ON gd.to_id = gp.id WHERE gp.segment_id = seg AND gp.alive AND gd.id IS NULL LOOP
      FOR id2, point2 IN SELECT gp.id, gp.point FROM db_point AS gp WHERE gp.segment_id = seg AND gp.alive AND gp.id <= id1 LOOP
         SELECT distance(point1, point2) INTO dist;
         INSERT INTO db_distance(fro_id, to_id, distance) VALUES (id2, id1, dist);
      END LOOP;
   END LOOP;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_counts(seg integer, variance real) RETURNS integer AS $$
DECLARE
   cnt integer;
   ident integer;
BEGIN
   UPDATE db_point SET count = 1;
   FOR ident IN SELECT id FROM db_point AS gp WHERE gp.segment_id = seg  LOOP
      SELECT COUNT(*) INTO cnt FROM db_distance AS gd WHERE (gd.fro_id=ident OR gd.to_id = ident) AND gd.distance <= variance;
      UPDATE db_point SET count = cnt WHERE id = ident;
   END LOOP;
   
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION grid_point_sample(seg integer)
RETURNS integer AS $$
DECLARE
   sampleSize integer;
   ident integer;
   ret integer;
   row db_point;
BEGIN
   sampleSize := 1;
   FOR ident IN SELECT (SELECT id FROM db_point 
                     WHERE probindex > r AND segment_id=seg 
                     ORDER BY probindex, score desc LIMIT 1)
             FROM (SELECT id, RANDOM() * 
                      (SELECT totalprob FROM db_segment 
                       WHERE id = seg LIMIT 1) AS r 
                   FROM db_point LIMIT sampleSize) AS tx LOOP
      ret := ident;
   END LOOP;
   RETURN ret;
END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION prune_new(seg integer, distClause text)
RETURNS integer AS $$
DECLARE
   ident integer;
   ident2 integer;
   pt real[];
   scre double precision;
   sql text;
BEGIN
   FOR ident, pt, scre IN SELECT id, point, score FROM db_point WHERE alive AND probIndex = 0.0 AND segment_id=seg ORDER BY score DESC LOOP
      sql := 'SELECT id FROM db_point AS gp WHERE ' || 
             distClause || 
            ' AND gp.alive AND gp.segment_id=$2 order by gp.score desc LIMIT 1';
      EXECUTE sql INTO ident2 USING pt,seg;
      IF ident = ident2 THEN
         sql := 'UPDATE db_point as gp SET alive=false WHERE gp.segment_id=$2 AND ' || distClause || ' AND gp.alive AND gp.id != $3'; 
         EXECUTE sql USING pt,seg,ident;
      ELSE
         UPDATE db_point SET alive=false WHERE id=ident;
      END IF;  
   END LOOP;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION traverse(seg integer, dim integer, center double precision, scale double precision, pt double precision[], 
OUT node db_partition, OUT upper double precision[], OUT lower double precision[])
AS $$
DECLARE
   idx integer;
   children boolean;
   tmp db_partition;
   next db_partition;
BEGIN
   upper := array_fill(center + scale, ARRAY[dim]);
   lower := array_fill(center - scale, ARRAY[dim]);
   SELECT * INTO node FROM db_partition WHERE segment_id=seg AND parent_id IS NULL;
   <<outer>>
   LOOP
      children := false;
      <<inner>>
      FOR tmp IN SELECT * FROM db_partition AS gp WHERE gp.parent_id=node.id AND gp.segment_id=seg LOOP
          children := true; 
          idx := tmp.index + 1;
          IF tmp.lower <= pt[idx] AND tmp.upper >= pt[idx] THEN
             next := tmp;
             EXIT inner;
          END IF;
      END LOOP;

      IF not children THEN
         EXIT outer;
      ELSE
         node := next;
         idx := node.index + 1;
         lower[idx] := node.lower;
         upper[idx] := node.upper;
      END IF;
   END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION compute_taylor(point integer, area double precision, temp double precision, rate double precision, depth integer)
RETURNS double precision[]
AS $$
DECLARE
   taylor double precision[];
   index integer;
   s double precision;
   fact double precision;
BEGIN
   taylor := array_fill(0.0, ARRAY[depth]);
   SELECT score INTO s FROM db_point WHERE id=point;
   s := s * rate;
   fact := 1.0;
   FOR index IN 1..depth LOOP
      BEGIN
         taylor[index] := area * pow(exp(s), temp) * pow(s, index - 1) / fact;
      EXCEPTION
         WHEN FLOATING_POINT_EXCEPTION THEN taylor[index] := 0.0;
         WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN taylor[index] := 0.0;
         WHEN DATA_EXCEPTION THEN taylor[index] := 0.0;
      END;
      fact := fact * index;
   END LOOP;
   RETURN taylor;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sum_taylor(seg integer, node_id integer, depth integer)
RETURNS double precision[]
AS $$
DECLARE
   index integer;
   current db_scoretree;
   child db_scoretree;
BEGIN
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND id=node_id;
   current.taylor = array_fill(0.0, ARRAY[depth]);
   FOR child IN SELECT * FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id LOOP
      FOR index IN SELECT generate_series(1, depth) LOOP
         current.taylor[index] := current.taylor[index] + child.taylor[index]; 
      END LOOP;
   END LOOP;
   RETURN current.taylor;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION propagate_taylor(seg integer, depth integer, node_id integer, tmp double precision, ofset integer, center double precision, depth2 integer)
RETURNS integer
AS $$
DECLARE
   numchildren integer;
   numleaves integer;
   maximum double precision;
   total double precision;
   value double precision;
   index integer;
   current db_scoretree;
   child db_scoretree;
BEGIN
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND id=node_id;
   LOOP
      total := 1e-300;
      numchildren := 0;
      numleaves := 0;
      maximum := -1e300;
      current.taylor = array_fill(0.0, ARRAY[depth]);
      FOR child IN SELECT * FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id LOOP
         FOR index IN SELECT generate_series(1, array_length(child.taylor, 1)) LOOP
            current.taylor[index] := current.taylor[index] + child.taylor[index]; 
         END LOOP;
         SELECT taylor_prob(current.taylor, depth2, ofset, center, tmp) INTO value;
         total := total + value;
--         numchildren := numchildren + 1 + child.child_count;
--         numleaves := numleaves + child.leaf_count;
--         IF child.max_score > maximum THEN maximum := child.max_score; END IF;
      END LOOP;

      value := value / total;
--      IF value > 1e-6 AND value < (1.0 - 1e-6) THEN
--         IF current.jump_link_id IS NOT NULL THEN
--            UPDATE db_partition SET jump_link_id=NULL WHERE jump_link_id=current.jump_link_id;
--         END IF;
--      END IF;

      UPDATE db_scoretree SET taylor=current.taylor WHERE id=current.id;

      IF current.parent_id IS NULL THEN EXIT;
      ELSE
         SELECT * INTO current FROM db_scoretree WHERE id=current.parent_id;
      END IF; 
   END LOOP;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION taylor_prob(coeffs double precision[], depth integer, ofset integer, center double precision, tmp double precision)
RETURNS double precision
AS $$
DECLARE
   total double precision;
BEGIN
   SELECT SUM(pow(tmp - center, p.index - 1) * coeffs[ofset + p.index]) INTO total FROM (SELECT generate_series(1, depth) AS index) AS p;
   RETURN total;
EXCEPTION
   WHEN FLOATING_POINT_EXCEPTION THEN RETURN 0.0;
   WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN RETURN 0.0;
   WHEN DATA_EXCEPTION THEN RETURN 0.0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION sample_taylor(seg integer, depth integer, ofset integer, center double precision, tmp double precision)
RETURNS integer
AS $$
DECLARE
   p1 double precision;
   p2 double precision;
   index integer;
   invalid boolean;
   children integer;
   current db_scoretree;
   child0 db_scoretree;
   child1 db_scoretree;
BEGIN
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND parent_id IS NULL;
   LOOP
      invalid := false;

      SELECT count(*) INTO children FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id;
      EXIT WHEN children = 0;

      SELECT * INTO child0 FROM db_scoretree WHERE parent_id=current.id AND segment_id=seg ORDER BY id LIMIT 1 OFFSET 0;
      SELECT * INTO child1 FROM db_scoretree WHERE parent_id=current.id AND segment_id=seg ORDER BY id LIMIT 1 OFFSET 1;

      SELECT taylor_prob(child0.taylor,depth,ofset,center,tmp) INTO p1;
      SELECT taylor_prob(child1.taylor,depth,ofset,center,tmp) INTO p2;
      BEGIN
         p1 := p1 / (1e-300 + p1 + p2);
      EXCEPTION
         WHEN FLOATING_POINT_EXCEPTION THEN invalid := true;
         WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN invalid := true;
         WHEN DATA_EXCEPTION THEN invalid := true;
      END;      

      IF invalid THEN  
         IF child0.taylor[1] > child1.taylor[1] THEN
            p1 := 1.0;
         ELSE
            IF child0.taylor[1] < child1.taylor[1] THEN
               p1 := 0.0;
            ELSE
               p1 := 0.5;
            END IF; 
         END IF; 
      END IF;
      
      SELECT RANDOM() INTO p2;
      IF p2 <= p1 THEN
         current := child0;
      ELSE
         current := child1;
      END IF;
   END LOOP;   
   
   RETURN current.point_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sample_tournament(seg integer, pressure double precision, rate double precision, tmp double precision)
RETURNS integer
AS $$
DECLARE
   p1 double precision;
   p2 double precision;
   children integer;
   current db_scoretree;
   child0 db_scoretree;
   child1 db_scoretree;
BEGIN
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND parent_id IS NULL;
   LOOP
      SELECT count(*) INTO children FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id;
      EXIT WHEN children = 0;
   
      SELECT * INTO child0 FROM db_scoretree WHERE parent_id=current.id AND segment_id=seg ORDER BY min_score DESC LIMIT 1 OFFSET 0;
      SELECT * INTO child1 FROM db_scoretree WHERE parent_id=current.id AND segment_id=seg ORDER BY min_score DESC LIMIT 1 OFFSET 1;


      BEGIN
         p1 := 1./(1. + pow(1 - pressure, rate * tmp * pow(2, child0.height)));
      EXCEPTION
         WHEN FLOATING_POINT_EXCEPTION THEN p1 := 1.0;
         WHEN NUMERIC_VALUE_OUT_OF_RANGE THEN p1 := 1.0;
         WHEN DATA_EXCEPTION THEN p1 := 1.0;
      END;
      IF p1 < 1.0 THEN
          p1 := (p1 / (1.0 - p1)) * child0.area;
          p1 := p1 / (p1 + child1.area);
      END IF;

      SELECT RANDOM() INTO p2;
      IF p2 <= p1 THEN
         current := child0;
      ELSE
         current := child1;
      END IF;
   END LOOP;   
   
   RETURN current.point_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION score_rotate_left(seg integer, node_id integer, propagate boolean, taylor_depth integer)
RETURNS integer
AS $$
DECLARE
   left db_scoretree;
   center db_scoretree;
   right db_scoretree;
   rightleft db_scoretree;
   rightright db_scoretree;
   rheight integer;
   lheight integer;
BEGIN
   SELECT * INTO center FROM db_scoretree WHERE segment_id=seg and id=node_id;
   SELECT * INTO left FROM db_scoretree WHERE segment_id=seg and parent_id=node_id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
   SELECT * INTO right FROM db_scoretree WHERE segment_id=seg and parent_id=node_id ORDER BY min_score DESC LIMIT 1 OFFSET 1;
   SELECT * INTO rightleft FROM db_scoretree WHERE segment_id=seg and parent_id=right.id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
   SELECT * INTO rightright FROM db_scoretree WHERE segment_id=seg and parent_id=right.id ORDER BY min_score DESC LIMIT 1 OFFSET 1;

   rightleft.parent_id := center.id;
   right.parent_id := center.parent_id;
   center.parent_id := right.id;

   center.area := left.area + rightleft.area;
   right.area := center.area + rightright.area;
   
   center.min_score := COALESCE(rightleft.min_score, left.max_score);
   center.max_score := left.max_score;
   right.min_score := COALESCE(rightright.min_score, center.max_score);
   right.max_score := center.max_score;

   center.child_count := left.child_count + COALESCE(rightleft.child_count,0) + 1;
   right.child_count := center.child_count + COALESCE(rightright.child_count,0) + 1;

   center.height := CASE WHEN left.height > rightleft.height THEN left.height ELSE rightleft.height END;
   right.height := CASE WHEN center.height > rightright.height THEN center.height ELSE rightright.height END;


   center.balance := center.balance + 1;
   IF right.balance < 0 THEN center.balance := center.balance - right.balance; END IF;

   right.balance := right.balance + 1;
   IF center.balance > 0 THEN right.balance := right.balance + center.balance; END IF;


   UPDATE db_scoretree SET parent_id=rightleft.parent_id WHERE id=rightleft.id;
   UPDATE db_scoretree SET parent_id=center.parent_id, balance=center.balance, area=center.area, min_score=center.min_score, max_score=center.max_score, child_count=center.child_count, height=center.height, taylor=sum_taylor(seg, center.id, taylor_depth) WHERE id=center.id;
   UPDATE db_scoretree SET parent_id=right.parent_id, balance=right.balance, area=right.area, min_score=right.min_score, max_score=right.max_score, child_count=right.child_count, height=right.height, taylor=sum_taylor(seg, right.id, taylor_depth) WHERE id=right.id;
   

--   SELECT compute_height(rightright.id) INTO rheight;
--   SELECT compute_height(center.id) INTO lheight;
--   IF right.balance != lheight - rheight THEN RETURN 0/0; END IF; 

--   SELECT compute_height(rightleft.id) INTO rheight;
--   SELECT compute_height(left.id) INTO lheight;
--   IF center.balance != lheight - rheight THEN RETURN 0/0; END IF; 

   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION score_rotate_right(seg integer, node_id integer, propagate boolean, taylor_depth integer)
RETURNS integer
AS $$
DECLARE
   right db_scoretree;
   center db_scoretree;
   left db_scoretree;
   leftleft db_scoretree;
   leftright db_scoretree;
   rheight integer;
   lheight integer;
BEGIN
   SELECT * INTO center FROM db_scoretree WHERE segment_id=seg and id=node_id;
   SELECT * INTO left FROM db_scoretree WHERE segment_id=seg and parent_id=node_id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
   SELECT * INTO right FROM db_scoretree WHERE segment_id=seg and parent_id=node_id ORDER BY min_score DESC LIMIT 1 OFFSET 1;
   SELECT * INTO leftleft FROM db_scoretree WHERE segment_id=seg and parent_id=left.id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
   SELECT * INTO leftright FROM db_scoretree WHERE segment_id=seg and parent_id=left.id ORDER BY min_score DESC LIMIT 1 OFFSET 1;

   leftright.parent_id := center.id;
   left.parent_id := center.parent_id;
   center.parent_id := left.id;

   center.area := right.area + leftright.area;
   left.area := center.area + leftleft.area;
   
   center.height := CASE WHEN right.height > leftright.height THEN right.height ELSE leftright.height END;
   left.height := CASE WHEN center.height > leftleft.height THEN center.height ELSE leftleft.height END;

   center.min_score := right.min_score;
   center.max_score := COALESCE(leftright.max_score, right.min_score);
   left.min_score := center.min_score;
   left.max_score := COALESCE(leftleft.max_score, center.min_score);

   center.child_count := COALESCE(leftright.child_count,0) + right.child_count + 1;
   left.child_count := center.child_count + COALESCE(leftleft.child_count,0) + 1;

   center.balance := center.balance - 1;
   IF left.balance > 0 THEN center.balance := center.balance - left.balance; END IF;

   left.balance := left.balance - 1;
   IF center.balance < 0 THEN left.balance := left.balance + center.balance; END IF;


   UPDATE db_scoretree SET parent_id=leftright.parent_id WHERE id=leftright.id;
   UPDATE db_scoretree SET parent_id=center.parent_id, balance=center.balance, area=center.area, min_score=center.min_score, max_score=center.max_score, child_count=center.child_count, height=center.height, taylor=sum_taylor(seg, center.id, taylor_depth) WHERE id=center.id;
   UPDATE db_scoretree SET parent_id=left.parent_id, balance=left.balance, area=left.area, min_score=left.min_score, max_score=left.max_score, child_count=left.child_count, height=left.height, taylor=sum_taylor(seg, left.id, taylor_depth) WHERE id=left.id;
   

--   SELECT compute_height(center.id) INTO rheight;
--   SELECT compute_height(leftleft.id) INTO lheight;
--   IF left.balance != lheight - rheight THEN RETURN 0/0; END IF; 

--   SELECT compute_height(right.id) INTO rheight;
--   SELECT compute_height(leftright.id) INTO lheight;
--   IF center.balance != lheight - rheight THEN RETURN 0/0; END IF; 

   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION compute_height(node_id integer)
RETURNS integer
AS $$
DECLARE
   current db_scoretree;
   height integer;
BEGIN
   height := 0;
   SELECT * INTO current FROM db_scoretree WHERE id=node_id;
   LOOP
      EXIT WHEN current.balance IS NULL;
      height := height + 1;
      IF current.balance > 0 THEN
         SELECT * INTO current FROM db_scoretree WHERE parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
      ELSE
         SELECT * INTO current FROM db_scoretree WHERE parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 1;
      END IF; 
   END LOOP;
   RETURN height;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION propagate_area(seg integer, node_id integer, inserted integer, taylor_depth integer)
RETURNS integer
AS $$
DECLARE
   current db_scoretree;
   left db_scoretree;
   right db_scoretree;
   oldbal integer;
   bal integer;
   cid integer;
   propagating integer;
   delta integer;
   fromLeft boolean;
   lheight integer;
   rheight integer;
BEGIN
-- Assumption is that we inserted at node_id, so that the parent_id of node_id changes in balance
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND id=node_id;
   propagating := inserted;
   fromLeft := true;
   LOOP
      
      SELECT * INTO left FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
      SELECT * INTO right FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 1;

--      IF inserted != 0 THEN
--      SELECT compute_height(right.id) INTO rheight;
--      SELECT compute_height(left.id) INTO lheight;
--      IF current.balance != lheight - rheight THEN RETURN 0/0; END IF; 
--      END IF;

--    Stop propagation when the balance switches from negative to positive or vice versa      

--    First check the balance
      IF inserted != 0 AND current.balance > 1 THEN
--       Heavy on the left
         IF left.balance > 0 THEN
            SELECT score_rotate_right(seg, current.id, false, taylor_depth) INTO delta;
         ELSE
            SELECT score_rotate_left(seg, left.id, false, taylor_depth) INTO delta;
            SELECT score_rotate_right(seg, current.id, false, taylor_depth) INTO delta;
         END IF;
         propagating := propagating - 1;
      ELSE
         IF inserted != 0 AND current.balance < -1 THEN
--          Heavy on the right
            IF right.balance < 0 THEN
               SELECT score_rotate_left(seg, current.id, false, taylor_depth) INTO delta;
            ELSE
               SELECT score_rotate_right(seg, right.id, false, taylor_depth) INTO delta;
               SELECT score_rotate_left(seg, current.id, false, taylor_depth) INTO delta;
            END IF;
            propagating := propagating - 1;
         ELSE
--          Balanced
            UPDATE db_scoretree SET area=left.area+right.area, child_count=left.child_count+right.child_count+1, min_score=right.min_score, max_score=left.max_score, taylor=sum_taylor(seg, id, taylor_depth) WHERE segment_id=seg AND id=current.id;
         END IF;
      END IF;
      
      IF inserted != 0 THEN      

      SELECT current.id = (SELECT id FROM db_scoretree WHERE segment_id=seg AND parent_id=current.parent_id ORDER BY min_score DESC LIMIT 1 OFFSET 0) INTO fromLeft;

      SELECT balance INTO oldbal FROM db_scoretree WHERE id=current.parent_id;
      UPDATE db_scoretree SET balance=balance+propagating WHERE id=current.parent_id and current.id = (SELECT id FROM db_scoretree WHERE segment_id=seg AND parent_id=current.parent_id ORDER BY min_score DESC LIMIT 1 OFFSET 0);
      UPDATE db_scoretree SET balance=balance-propagating WHERE id=current.parent_id and current.id = (SELECT id FROM db_scoretree WHERE segment_id=seg AND parent_id=current.parent_id ORDER BY min_score DESC LIMIT 1 OFFSET 1);
      SELECT balance INTO bal FROM db_scoretree WHERE id=current.parent_id;

      IF oldbal < 0 AND bal >= 0 THEN propagating := 0; END IF;
      IF oldbal > 0 AND bal <= 0 THEN propagating := 0; END IF;

      UPDATE db_scoretree SET height=height+propagating WHERE id=current.parent_id;      

      END IF;

      IF current.parent_id IS NULL THEN EXIT;
      ELSE
         SELECT * INTO current FROM db_scoretree WHERE id=current.parent_id;
      END IF; 
   END LOOP;
   RETURN 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION traverse_score_tree(seg integer, score double precision)
RETURNS integer
AS $$
DECLARE
   children integer;
   left db_scoretree;
   right db_scoretree;
   current db_scoretree;
BEGIN
   SELECT * INTO current FROM db_scoretree WHERE segment_id=seg AND parent_id IS NULL;
   LOOP      
      SELECT count(*) INTO children FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id;
      EXIT WHEN children = 0;

      SELECT * INTO left FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 0;
      SELECT * INTO right FROM db_scoretree WHERE segment_id=seg AND parent_id=current.id ORDER BY min_score DESC LIMIT 1 OFFSET 1;

      IF score > right.max_score THEN
         current := left;
      ELSE
         current := right;
      END IF;
   END LOOP;
   RETURN current.id;
END;
$$ LANGUAGE plpgsql;

